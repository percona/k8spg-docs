#!/usr/bin/env python3
"""
Uses the mingrammer *diagrams* library with Kubernetes node icons:
https://diagrams.mingrammer.com/docs/nodes/k8s

Prerequisites:
  pip install diagrams
  # Graphviz must be installed (provides the `dot` binary):
  #   macOS: brew install graphviz
  #   Debian/Ubuntu: apt-get install graphviz

Run from repo root:
  python docs/assets/diagrams/operator_flow.py
  python docs/assets/diagrams/operator_flow.py --format png
  python docs/assets/diagrams/operator_flow.py --format both

Default output: docs/assets/images/operator-flow-diagram.png.

Colors and cluster framing follow docs/assets/images/operator.svg (light blue fill #d4edfb,
cluster stroke #729fcf, connector blue #3465a4, label text #092256).
"""

from __future__ import annotations

import argparse
from pathlib import Path

from diagrams import Cluster, Diagram, Edge
from diagrams.k8s.compute import Pod, Deployment
from diagrams.k8s.others import CRD

# Resolve paths so the script works when run from any cwd
_HERE = Path(__file__).resolve().parent
_REPO_ROOT = _HERE.parents[2]
_OUT_DIR = _REPO_ROOT / "docs" / "assets" / "images"
_OUT_NAME = "operator-flow-diagram"

# Palette aligned with docs/assets/images/operator.svg (Percona operator diagram)
_BG = "#ffffff"
_CLUSTER_FILL = "#d4edfb"  # rgb(212, 237, 251)
_CLUSTER_BORDER = "#729fcf"  # rgb(114, 159, 207)
# Primary UI blue in operator.svg (trapezoids / hex icons): rgb(50, 108, 229) — built-in K8s PNG icons match this.
_EDGE = "#3465a4"  # rgb(52, 101, 164) — connectors and arrows
_TEXT = "#092256"  # rgb(9, 34, 87) — titles and labels


def _cluster_graph_attr() -> dict[str, str]:
    """Rounded cluster box like the large light-blue area in operator.svg."""
    return {
        "bgcolor": _CLUSTER_FILL,
        "style": "rounded",
        "color": _CLUSTER_BORDER,
        "penwidth": "2",
        "fontcolor": _TEXT,
        "fontsize": "13",
    }


def _graph_attr_for_format(outformat: str) -> dict[str, str]:
    """Graphviz graph attributes; PNG sets dpi for readable raster output."""
    ga: dict[str, str] = {
        "bgcolor": _BG,
        "pad": "0.45",
        "fontsize": "13",
        "fontname": "Helvetica",
    }
    if outformat == "png":
        ga["dpi"] = "150"
    return ga


def _build(outformat: str) -> Path:
    """Write operator-flow-diagram.{svg|png} to docs/assets/images/."""
    if outformat not in ("svg", "png"):
        raise ValueError(f"unsupported format: {outformat!r}")

    _OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = str(_OUT_DIR / _OUT_NAME)

    graph_attr = _graph_attr_for_format(outformat)

    node_attr = {
        "fontcolor": _TEXT,
        "fontsize": "12",
        "fontname": "Helvetica",
    }

    edge_attr = {
        "color": _EDGE,
        "fontcolor": _TEXT,
        "fontsize": "10",
        "fontname": "Helvetica",
        "penwidth": "1.5",
    }

    # Left-to-right main flow (CRD → … → Application); colors match operator.svg
    with Diagram(
        "",
        filename=out_path,
        show=False,
        direction="LR",
        graph_attr=graph_attr,
        node_attr=node_attr,
        edge_attr=edge_attr,
        outformat=outformat,
    ):
        with Cluster("Kubernetes Cluster", graph_attr=_cluster_graph_attr()):
            crd = CRD("Custom Resource\nDefinition (CRD)")
            # No dedicated "Custom Resource instance" icon in k8s provider; Pod denotes workload API objects.
            custom_resources = CRD("Custom Resources")
            operator = Deployment("Operator Deployment")

            # Pods left-to-right: disconnected nodes in an LR subgraph share one rank and
            # stack vertically; chain with invisible edges to fix order (diagrams Cluster
            # + Graphviz limitation — see Cluster docstring in mingrammer/diagrams).
            with Cluster(
                "Application",
                direction="LR",
                graph_attr=_cluster_graph_attr(),
            ):
                # Three workload replicas (labels echo operator.svg DB Pod 1 / 2 / N pattern).
                app_pod_1 = Pod("DB Pod 1")
                app_pod_2 = Pod("DB Pod 2")
                app_pod_n = Pod("DB Pod N")
                app_pod_1 >> Edge(style="invis") >> app_pod_2 >> Edge(style="invis") >> app_pod_n

            # CRD defines schema available to the API; users then create CR instances.
            crd >> Edge(label="defines schema", color=_EDGE) >> custom_resources

            # Bidirectional: Operator watches CRs and reconciles cluster state.
            custom_resources << Edge(
                forward=True,
                reverse=True,
                label="watch / reconcile",
                color=_EDGE,
            ) >> operator

            # Operator drives the managed application (StatefulSets, Services, etc.).
            operator >> Edge(label="manages", color=_EDGE) >> app_pod_1

    return _OUT_DIR / f"{_OUT_NAME}.{outformat}"


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Render the operator control-flow diagram (CRD → … → Application).",
    )
    p.add_argument(
        "-f",
        "--format",
        choices=("svg", "png", "both"),
        default="png",
        help="Output format: vector SVG, raster PNG, or both (default: png).",
    )
    return p.parse_args()


def main() -> None:
    args = _parse_args()
    if args.format == "both":
        paths = [_build("svg"), _build("png")]
    else:
        paths = [_build(args.format)]
    for path in paths:
        print(f"Wrote {path}")


if __name__ == "__main__":
    main()
