import networkx as nx
import matplotlib.pyplot as plt

# Turing Machine class definition
class TuringMachine:
    def __init__(self, tape="", blank="_", initial_state="", max_cell_writes=None, max_head_turns=None):
        self.tape = list(tape)
        self.blank = blank
        self.head_position = 0
        self.state = initial_state
        self.transition = {}
        self.cell_write_count = {i: 0 for i in range(len(tape))}
        self.head_turns = 0
        self.last_move = None
        self.max_cell_writes = max_cell_writes
        self.max_head_turns = max_head_turns

    def add_transition(self, state, char, new_char, move, new_state):
        self.transition[(state, char)] = (new_char, move, new_state)

    def step(self):
        char = self.tape[self.head_position]
        action = self.transition.get((self.state, char))
        if action:
            new_char, move, new_state = action
            if self.max_cell_writes is not None and self.cell_write_count[self.head_position] >= self.max_cell_writes:
                print("Exceeded maximum cell writes at position:", self.head_position)
                self.state = "HALT"
                return
            if self.max_head_turns is not None and self.last_move != move and self.last_move is not None:
                self.head_turns += 1
                if self.head_turns > self.max_head_turns:
                    print("Exceeded maximum head turns.")
                    self.state = "HALT"
                    return
            self.last_move = move
            self.tape[self.head_position] = new_char
            self.cell_write_count[self.head_position] += 1
            if move == 'R':
                self.head_position += 1
            elif move == 'L':
                self.head_position -= 1
            self.state = new_state
            if self.head_position < 0:
                self.tape.insert(0, self.blank)
                self.head_position = 0
            elif self.head_position >= len(self.tape):
                self.tape.append(self.blank)

    def run(self, max_steps=10000):
        steps = 0
        while steps < max_steps and self.state != "HALT":
            self.step()
            steps += 1

def create_graph():
    G = nx.DiGraph()
    num_edges = int(input("How many edges in your graph? "))
    print("Enter edges in the format: start end (e.g., 0 1)")
    for _ in range(num_edges):
        edge = input("Enter edge: ").split()
        G.add_edge(int(edge[0]), int(edge[1]))
    return G

def plot_graph(graph):
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True, node_color='skyblue', edge_color='black')
    plt.title("Decorated Graph Visualization")
    plt.show()

def main():
    # Turing Machine interaction
    tape = input("Enter the initial tape: ")
    initial_state = input("Enter the initial state: ")
    max_cell_writes = int(input("Enter the maximum number of writes per cell: "))
    max_head_turns = int(input("Enter the maximum number of head turns: "))

    machine = TuringMachine(tape=tape, initial_state=initial_state, max_cell_writes=max_cell_writes, max_head_turns=max_head_turns)
    machine.add_transition("init", "1", "0", "R", "next")
    machine.add_transition("next", "0", "1", "L", "init")
    machine.add_transition("next", "1", "1", "R", "HALT")
    machine.run()
    print("Tape after processing:", "".join(machine.tape))

    # Graph creation and visualization
    graph = create_graph()
    plot_graph(graph)

if __name__ == "__main__":
    main()
