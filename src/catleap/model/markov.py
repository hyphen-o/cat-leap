from collections import defaultdict

def count_transitions(sequence, n):
    transitions = defaultdict(lambda: defaultdict(int))
    for i in range(len(sequence) - n):
        current_state = tuple(sequence[i:i+n])
        next_state = sequence[i+n]
        transitions[current_state][next_state] += 1
    return transitions

def predict_next_state(transitions, current_state):
    next_states = transitions.get(tuple(current_state), {})
    if not next_states:
        return None
    return max(next_states, key=next_states.get)

sequence = [0, 1, 2, 3, 2, 1, 0, 1, 2, 3, 4, 3, 2, 1, 0]

transitions = count_transitions(sequence, 2)

current_state = [1, 2]
predicted_next_state = predict_next_state(transitions, current_state)
