import matplotlib.pyplot as plt

class KDNode:
    def __init__(self, point, left=None, right=None):
        self.point = point
        self.left = left
        self.right = right


def build_kdtree(points, depth=0):
    if not points:
        return None

    k = len(points[0])
    axis = depth % k

    points.sort(key=lambda x: x[axis])
    median = len(points) // 2

    return KDNode(
        point=points[median],
        left=build_kdtree(points[:median], depth + 1),
        right=build_kdtree(points[median + 1:], depth + 1)
    )


def plot_kdtree(node, depth=0, bounds=(0, 10, 0, 10), ax=None):
    if node is None:
        return

    x_min, x_max, y_min, y_max = bounds
    x, y = node.point
    axis = depth % 2

    if axis == 0:
        # vertical split
        ax.plot([x, x], [y_min, y_max], 'r--')
        plot_kdtree(node.left, depth + 1, (x_min, x, y_min, y_max), ax)
        plot_kdtree(node.right, depth + 1, (x, x_max, y_min, y_max), ax)
    else:
        # horizontal split
        ax.plot([x_min, x_max], [y, y], 'b--')
        plot_kdtree(node.left, depth + 1, (x_min, x_max, y_min, y), ax)
        plot_kdtree(node.right, depth + 1, (x_min, x_max, y, y_max), ax)

    ax.plot(x, y, 'ko')  # draw the point


if __name__ == "__main__":
    pontos = [(2, 3), (5, 4), (9, 6), (4, 7), (8, 1), (7, 2)]
    arvore = build_kdtree(pontos)

    fig, ax = plt.subplots()
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_aspect('equal')
    ax.set_title("2D KD-Tree Visualization")
    plot_kdtree(arvore, ax=ax)
    plt.show()
