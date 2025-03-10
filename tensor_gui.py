import torch
import torch.nn as nn
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.backends.backend_tkagg as tkagg
from einops import rearrange
import re
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"


class ModelVisualizer:
    def __init__(
            self, 
            model, 
            forward_fn=None, 
            max_runs=2,
            tensor_reshape_funcs={
                ".+\.attentions\.0\.transformer_blocks\.0\.attn[012]\.to_out\.[01]": lambda x:rearrange(x, "b (h w) e -> b h w e", h=int(x.shape[1]**0.5), w=int(x.shape[1]**0.5))
            },
        ):
        self.model = model
        self.forward_fn = forward_fn
        self.curr_run_id = 0
        self.max_runs = max_runs
        self.tensor_reshape_funcs = tensor_reshape_funcs
        self.activations = [{}]
        self._register_hooks()

    def _get_activation_hook(self, name):
        def hook(model, input, output):
            if isinstance(output, (list, tuple)):
                for i, out in enumerate(output):
                    if isinstance(output, torch.Tensor):
                        self.activations[-1][f"{name}_{i}"] = out.detach().cpu()
                        # TODO: Handle multiple outputs types
            if isinstance(output, torch.Tensor):
                output = output.detach().cpu()
                for pat in self.tensor_reshape_funcs:
                    if re.compile(pat).match(name):
                        output = self.tensor_reshape_funcs[pat](output)
                self.activations[-1][name] = output
        return hook

    def _register_hooks(self):
        for name, module in self.model.named_modules():
            module.register_forward_hook(self._get_activation_hook(name))

    def register_inc_id_hook(self, module):
        def _hook(_m, input, output):
            self.inc_run_id()
        module.register_forward_hook(_hook)

    def inc_run_id(self, n=1):
        self.curr_run_id += n
        self.activations.append({})
        if len(self.activations) > self.max_runs + 1:
            self.activations.pop(0)

    def run_inference(self, input_data_list):
        assert self.forward_fn is not None, "Forward function not provided."
        with torch.no_grad():
            for d in input_data_list:
                self.forward_fn(self.model, d)
                self.inc_run_id()
    
    def __len__(self):
        return len(self.activations) - 1


class GUI:
    def __init__(self, visualizer: ModelVisualizer):
        self.visualizer = visualizer
        self.root = tk.Tk()
        self.root.title("PyTorch Model Visualizer")
        self.root.geometry("800x600")

        self.root.rowconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=1)

        self.run_selector = ttk.Combobox(self.root, values=[f"Run {i}" for i in range(len(visualizer))])
        self.run_selector.current(0)
        self.run_selector.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        self.run_selector.bind('<<ComboboxSelected>>', self.update_activation_list)

        frame = tk.Frame(self.root)
        frame.grid(row=1, column=0, sticky="nsew")
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

        self.act_listbox = tk.Listbox(frame)
        self.act_listbox.grid(row=0, column=0, sticky="nsew")

        self.weight_listbox = tk.Listbox(frame)
        self.weight_listbox.grid(row=0, column=1, sticky="nsew")

        for name, _ in self.visualizer.model.named_parameters():
            self.weight_listbox.insert(tk.END, name)

        self.update_activation_list()

        visualize_button = tk.Button(self.root, text="Visualize", command=self.visualize_tensor)
        visualize_button.grid(row=1, column=0, sticky="ew")

        self.root.mainloop()

    def update_activation_list(self, event=None):
        self.act_listbox.delete(0, tk.END)
        run_id = int(self.run_selector.get().split()[1])
        for act_name in self.visualizer.activations[run_id]:
            self.act_listbox.insert(tk.END, act_name)

    def visualize_tensor(self):
        selected_weight = self.weight_listbox.curselection()
        selected_act = self.act_listbox.curselection()

        if selected_weight:
            tensor_name = self.weight_listbox.get(selected_weight)
            tensor = dict(self.visualizer.model.named_parameters())[tensor_name].detach().cpu()
        elif selected_act:
            run_id = int(self.run_selector.get().split()[1])
            tensor_name = self.act_listbox.get(selected_act)
            tensor = self.visualizer.activations[run_id][tensor_name]
        else:
            messagebox.showerror("Error", "Select an activation or weight to visualize.")
            return

        TensorVisualizer(tensor, tensor_name)


class TensorVisualizer:
    def __init__(self, tensor, name):
        self.tensor = tensor
        self.name = name

        self.root = tk.Toplevel()
        self.root.title(f"Tensor Visualization - {name}")

        if self.tensor.ndim <= 2:
            self.display_heatmap()
        else:
            self.dim_selections = []
            self.index_entries = []

            tk.Label(self.root, text="Select up to 2 dimensions for visualization (others: indices)").pack()
            for dim in range(self.tensor.ndim):
                frame = tk.Frame(self.root)
                frame.pack(anchor='w')
                var = tk.IntVar()
                chk = tk.Checkbutton(frame, text=f"Dim {dim} (Size={self.tensor.size(dim)})", variable=var)
                chk.pack(side=tk.LEFT)
                entry = tk.Entry(frame, width=5)
                entry.pack(side=tk.LEFT)
                entry.insert(0, "0")
                self.dim_selections.append(var)
                self.index_entries.append(entry)

            self.agg_or_index = ttk.Combobox(self.root, values=['mean', 'max', 'min', 'median', 'sum', 'select indices'])
            self.agg_or_index.current(0)
            self.agg_or_index.pack()

            confirm_button = tk.Button(self.root, text="Confirm", command=self.display_heatmap)
            confirm_button.pack()

    def display_heatmap(self):
        if self.tensor.ndim <= 2:
            tensor_agg = self.tensor
            dims_to_agg = []
            var_tensor = torch.zeros_like(tensor_agg)
        else:
            selected_dims = [i for i, v in enumerate(self.dim_selections) if v.get()]
            if len(selected_dims) > 2:
                messagebox.showerror("Error", "Select at most two dimensions.")
                return

            agg_choice = self.agg_or_index.get()
            dims_to_agg = [i for i in range(self.tensor.ndim) if i not in selected_dims]

            if agg_choice == 'select indices':
                idx = []
                for dim in range(self.tensor.ndim):
                    if dim in dims_to_agg:
                        entry_val = self.index_entries[dim].get()
                        try:
                            index = int(entry_val)
                            if index < 0 or index >= self.tensor.size(dim):
                                raise ValueError
                            idx.append(index)
                        except ValueError:
                            messagebox.showerror("Error", f"Invalid index for dimension {dim}")
                            return
                    else:
                        idx.append(slice(None))
                tensor_agg = self.tensor[tuple(idx)].squeeze()
                var_tensor = torch.zeros_like(tensor_agg)
            else:
                agg_method = getattr(torch, agg_choice)
                tensor_agg = agg_method(self.tensor, dim=dims_to_agg, keepdim=False)
                var_tensor = torch.var(self.tensor, dim=dims_to_agg)

        _, ax = plt.subplots(1, 2, figsize=(12, 6))
        im0 = ax[0].imshow(tensor_agg.numpy(), aspect='auto', cmap='viridis')
        ax[0].set_title(f"{self.name} Aggregated Values")
        plt.colorbar(im0, ax=ax[0])

        im1 = ax[1].imshow(var_tensor.numpy(), aspect='auto', cmap='magma')
        ax[1].set_title(f"{self.name} Variance")
        plt.colorbar(im1, ax=ax[1])

        plt.tight_layout()
        plt.show()


def forward_fn(model, input_data):
    return model(input_data)


if __name__ == "__main__":
    model = nn.Sequential(
        nn.Conv2d(3, 8, 3, 1, 1),
        nn.ReLU(),
        nn.AdaptiveAvgPool2d(1),
        nn.Flatten(),
        nn.Linear(8, 10)
    )
    input_data_list = [
        torch.randn(1, 3, 32, 32),
        torch.randn(1, 3, 224, 224),
        torch.randn(1, 3, 512, 512),
    ]

    visualizer = ModelVisualizer(model, forward_fn)
    visualizer.run_inference(input_data_list)

    gui = GUI(visualizer)
