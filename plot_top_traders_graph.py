import sys
import networkx as nx
import plotly.graph_objects as go
import numpy as np
from collections import deque
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from config import (EXCLUDED_ADDRESSES, EDGE_POINTS_QUANTITY,
                    EDGE_POINTS_OPACITY)

# References:
# - https://stackoverflow.com/questions/74607000/python-networkx-plotly-how-to-display-edges-mouse-over-text
# - https://stackoverflow.com/questions/49234144/networkx-node-size-must-correlate-to-dimension
# - https://matplotlib.org/stable/users/explain/colors/colormaps.html


def weight_to_color(weight,
                    min_weight,
                    max_weight,
                    cmap=plt.cm.viridis,
                    use_log=True):
    """Function to map weight to a color using a colormap."""

    if use_log:
        log_weight = np.log10(weight)
        norm = mcolors.Normalize(vmin=np.log10(min_weight),
                                 vmax=np.log10(max_weight))

        return mcolors.to_hex(cmap(norm(log_weight)))
    else:
        norm = mcolors.Normalize(vmin=min_weight, vmax=max_weight)

        return mcolors.to_hex(cmap(norm(weight)))


def create_plotly_graph(G, pos, nodes, wallet_address_edges_count_dict):

    # Get count list
    counts = list(wallet_address_edges_count_dict.values())
    min_count = min(counts)
    max_count = max(counts)

    # Create edge traces
    edge_x = []
    edge_y = []

    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(x=edge_x,
                            y=edge_y,
                            line=dict(width=1, color='gray'),
                            hoverinfo='none',
                            mode='lines')

    # Create node traces
    node_x = []
    node_y = []
    node_color = []
    node_text = []
    node_sizes = []

    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

        # Determine color and hover text based on attributes
        if node in nodes:
            attributes = nodes[node]
            node_color.append('red')
            node_sizes.append(50)
            node_text.append('<br>'.join(
                [f"{key}: {value}" for key, value in attributes.items()]))
        else:
            weighted_colour = weight_to_color(
                wallet_address_edges_count_dict[node],
                min_count,
                max_count,
                cmap=plt.cm.plasma,
                use_log=False)
            node_color.append(weighted_colour)
            node_sizes.append(20)
            node_text.append(node)

    node_trace = go.Scatter(x=node_x,
                            y=node_y,
                            mode='markers',
                            marker=dict(size=node_sizes,
                                        color=node_color,
                                        line=dict(width=2, color='black')),
                            text=node_text,
                            hoverinfo='text',
                            hoverlabel=dict(font=dict(size=24)))

    colorbar_trace = go.Scatter(
        x=[None],
        y=[None],
        mode='markers',
        marker=dict(
            colorscale='Plasma',
            cmin=min_count,
            cmax=max_count,
            colorbar=dict(
                title='No. of Connections from Wallet Address',
                titleside='right',
                thickness=15,
                tickvals=[min_count, max_count],
                ticktext=[f'{min_count}', f'{max_count}'],
                tickformat='d',
                tickmode='array',
                x=1.05,  # Position to the right of the first colorbar
                y=0.5,  # Centering the colorbar vertically
                len=0.75)),
        showlegend=False,
        hoverinfo='none')

    # Combine edge and node traces into a Plotly Figure
    fig = go.Figure(data=[edge_trace, node_trace, colorbar_trace])

    # Add layout details
    fig.update_layout(showlegend=False,
                      xaxis=dict(showgrid=False, zeroline=False),
                      yaxis=dict(showgrid=False, zeroline=False),
                      plot_bgcolor='white',
                      margin=dict(l=40, r=40, t=40, b=40))

    return fig


def plot_nodes_edges_graph(graph_data, repeated_wallets_dict):

    G = nx.DiGraph()

    nodes = graph_data.get('nodes', {})
    edges = graph_data.get('edges', {})

    for edge in edges:
        mint_address, wallet_address = edge.split('-')

        if wallet_address in EXCLUDED_ADDRESSES:
            continue

        if wallet_address in repeated_wallets_dict:
            G.add_node(wallet_address)
            G.add_edge(mint_address, wallet_address)

    for node, attributes in nodes.items():
        G.add_node(node, **attributes)

    pos = nx.spiral_layout(G,
                           scale=1,
                           center=None,
                           dim=2,
                           resolution=0.8,
                           equidistant=True)

    fig = create_plotly_graph(G, pos, nodes, repeated_wallets_dict)
    fig.show()
