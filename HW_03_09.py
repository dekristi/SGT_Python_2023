import random

def generate_friendship_graph(num_users, avg_connections):
    friendship_graph = {}

    for user in range(1, num_users + 1):
        num_connections = random.randint(1, 2 * avg_connections)
        connections = random.sample(range(1, num_users + 1), num_connections)
        try:
            connections.remove(user)  # Remove self-connection
        except:
            pass
        friendship_graph[user] = connections

    return friendship_graph

def save_friendship_graph_to_file(friendship_graph, filename):
    with open(filename, 'w') as file:
        for user, connections in friendship_graph.items():
            connections_str = ' '.join(map(str, connections))
            file.write(f"{user} {connections_str}\n")

if name == "main":
    num_users = 1000  # Change this to the desired number of users
    avg_connections = 30  # Change this to the desired average number of connections per user
    output_filename = "follower_graph.txt"

    graph = generate_friendship_graph(num_users, avg_connections)
    save_friendship_graph_to_file(graph, output_filename)
    print(f"Friendship graph with {num_users} users saved to {output_filename}.")