import matplotlib.pyplot as plt
import os

def generate_vendor_graph(medicine_name):

    # Example vendor availability
    vendors = [
        "Apollo",
        "MedPlus",
        "NetMeds",
        "Wellness"
    ]

    # 1 = Available, 0 = Not Available
    availability = [1, 1, 0, 1]

    colors = []

    for value in availability:
        if value == 1:
            colors.append("green")
        else:
            colors.append("red")

    # Create figure
    plt.figure(figsize=(18,8))

    # ---------------- BAR GRAPH ----------------
    plt.subplot(1,2,1)

    bars = plt.bar(vendors, availability, color=colors)

    plt.title(f"{medicine_name} Availability")

    plt.yticks([0,1], ["Not Available", "Available"])

    for bar in bars:

        height = bar.get_height()

        if height == 1:
            label = "Available"
        else:
            label = "Not Available"

        plt.text(
            bar.get_x() + bar.get_width()/2,
            height + 0.02,
            label,
            ha='center'
        )

    # ---------------- PIE CHART ----------------
    plt.subplot(1,2,2)

    available_count = availability.count(1)
    unavailable_count = availability.count(0)

    plt.pie(
        [available_count, unavailable_count],
        labels=["Available", "Not Available"],
        autopct='%1.1f%%'
    )

    plt.title("Availability Percentage")

    # Save graph
    if not os.path.exists("static"):
        os.makedirs("static")

    graph_path = os.path.join("static", "vendor_graph.png")

    plt.tight_layout()

    plt.savefig(graph_path)

    plt.close()

    return graph_path