import plotly.graph_objects as go
from py3dbp import Bin


def plot_packer_3d(bin: Bin):
    fig = go.Figure()

    for item in bin.items:
        x, y, z = [float(p) for p in item.position]
        w, h, d = float(item.width), float(item.height), float(item.depth)

        color = item.color or "#1f77b4"

        # Create the cuboid as a transparent mesh (edges only)
        fig.add_trace(
            go.Mesh3d(
                x=[x, x + w, x + w, x, x, x + w, x + w, x],
                y=[y, y, y + h, y + h, y, y, y + h, y + h],
                z=[z, z, z, z, z + d, z + d, z + d, z + d],
                color=color,
                opacity=1,
                flatshading=False,
                alphahull=0,
                showscale=False,
                name=item.name,
                hovertext=f"{item.partno} ({w}x{h}x{d})",
                hoverinfo="text",
            )
        )

    # Add pallet wireframe
    W, H, D = bin.width, bin.height, bin.depth
    fig.add_trace(
        go.Mesh3d(
            x=[0, W, W, 0, 0, W, W, 0],
            y=[0, 0, H, H, 0, 0, H, H],
            z=[0, 0, 0, 0, D, D, D, D],
            color="rgba(0,0,0,0)",
            opacity=0.1,
            alphahull=0,
            flatshading=True,
            hoverinfo="skip",
            name="Pallet",
        )
    )

    fig.update_layout(
        title="3D Packed Bin Visualization",
        scene=dict(
            xaxis_title="X (Width)",
            yaxis_title="Y (Height)",
            zaxis_title="Z (Depth)",
            aspectratio=dict(x=W / D, y=H / D, z=1),
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.5)),
        ),
        margin=dict(l=0, r=0, b=0, t=30),
        showlegend=False,
    )

    fig.show()
