import numpy as np
import matplotlib.pyplot as plt

# Constants
C = 299792458  # Speed of light in m/s
delta_t = 5
h = 6.62607015e-34  # Planck's constant in m^2 kg / s

class GlobalTime:
    def __init__(self):
        self.phi_history = [0] * delta_t  # Initialize Φ history for the delay period
        self.current_time = 0
        self.time_flow_rate = 1
        self.dt = 0.01  # Small time step for RK4
        self.time_flow_rates = []  # Keep track of time flow rate for plotting

    def calculate_phi_derivative(self, particles):
        phi_delayed = self.phi_history[-delta_t]
        s_t = np.random.normal(0, 0.01)  # Simulate spontaneous fluctuations
        g_phi_t = -0.1 * phi_delayed  # Generative faculty adjustment
        states = np.array([p.state for p in particles])
        mean_state = np.mean(states, axis=0)
        variance = np.var(states, axis=0)
        # Directive and adaptive faculties influence
        return s_t + g_phi_t + np.linalg.norm(mean_state) + np.linalg.norm(variance)

    def update_phi(self, particles):
        # Update Φ using a 4th-order Runge-Kutta method
        k1 = self.dt * self.calculate_phi_derivative(particles)
        k2 = self.dt * self.calculate_phi_derivative(particles)  # Corrected call
        k3 = self.dt * self.calculate_phi_derivative(particles)  # Corrected call
        k4 = self.dt * self.calculate_phi_derivative(particles)  # Corrected call
        phi_update = (k1 + 2*k2 + 2*k3 + k4) / 6
        self.phi_history.append(self.phi_history[-1] + phi_update)
        if len(self.phi_history) > delta_t:
            self.phi_history.pop(0)

    def update_time_flow(self):
        current_phi = self.phi_history[-1]
        k = 0.05  # Sensitivity factor for Φ's effect on time flow rate
        self.time_flow_rate = 1 + k * np.tanh(current_phi)
        self.time_flow_rates.append(self.time_flow_rate)  # For plotting

    def update_current_time(self):
        self.current_time += self.time_flow_rate * self.dt



class QuantumParticle:
    def __init__(self, state, velocity):
        self.state = np.array(state, dtype=np.float64)  # Assuming a vector state for simplicity
        self.velocity = np.array(velocity, dtype=np.float64)  # Particle velocity
        # Simplified model for Hamiltonian dynamics; real applications would need specific H
        self.H = np.eye(len(state))  # Identity matrix as placeholder
        self.dilated_times = []  # Tracking dilated time for visualization

    def update_state(self, dt, global_time):
        # Update quantum state based on ATH-modified Lorentz factor and Hamiltonian
        lorentz_factor = 1 / np.sqrt(1 - np.linalg.norm(self.velocity)**2 / C**2)  # Classical Lorentz factor
        # Integrate ATH effect
        lorentz_factor_ath = lorentz_factor * (1 + global_time.phi_history[-1])
        effective_dt = dt * lorentz_factor_ath
        # Simplified quantum state evolution; real dynamics would involve solving Schrödinger's equation
        self.state = self.state + np.dot(self.H, self.state) * effective_dt
        self.state /= np.linalg.norm(self.state)  # Normalize the state

    def calculate_dilated_time(self, dt, global_time):
        # Calculate time dilation using ATH-modified Lorentz factor
        lorentz_factor = 1 / np.sqrt(1 - np.linalg.norm(self.velocity)**2 / C**2)
        lorentz_factor_ath = lorentz_factor * (1 + global_time.phi_history[-1])
        dilated_time = dt * lorentz_factor_ath
        self.dilated_times.append(dilated_time)  # For visualization
        return dilated_time


class ActiveTimeEffect:
    def __init__(self, ath_parameter):
        self.ath_parameter = ath_parameter  # Parameter to represent ATH effect

    def modify_lorentz_factor(self, velocity):
        # Modify Lorentz factor for time dilation with ATH effect
        gamma = 1 / np.sqrt(1 - (velocity / C)**2)
        return gamma * (1 + self.ath_parameter)

    def modify_energy_levels(self, particle, gamma):
        # Modify energy levels of the particle based on ATH-influenced Lorentz factor
        # Check if the object is a CesiumAtom and use the correct attribute
        if isinstance(particle, CesiumAtom):
            modified_levels = [E * gamma for E in particle.energy_levels]
        else:
            modified_levels = [E * gamma for E in particle.energy_states]
        return modified_levels


class CesiumAtom:
    def __init__(self):
        # Define cesium energy levels (example values)
        self.energy_levels = [-1.84e-23, -1.81e-23, -1.78e-23]
    
    def calculate_transitions(self):
        # Compute transition frequencies
        self.transition_frequencies = {}
        for i in range(len(self.energy_levels)):
            for j in range(i+1, len(self.energy_levels)):
                freq = (self.energy_levels[j] - self.energy_levels[i]) / h
                self.transition_frequencies[(i, j)] = freq

def run_simulation(use_active_time, max_iterations=1000):
    global_time = GlobalTime()
    ath_effect = ActiveTimeEffect(0.05)  # Example ATH parameter
    cesium_atoms = [CesiumAtom() for _ in range(5)]
    particles = [QuantumParticle([1.0, 0.0], np.random.uniform(-0.1, 0.1, 3) * C) for _ in range(5)]
    intrinsic_times = []

    for iteration in range(max_iterations):
        if use_active_time:
            global_time.update_phi(particles)
            global_time.update_time_flow()
            global_time.update_current_time()

            # Apply ATH effects on cesium atoms
            for atom in cesium_atoms:
                gamma = ath_effect.modify_lorentz_factor(0.1 * C)  # Example velocity
                atom.energy_levels = ath_effect.modify_energy_levels(atom, gamma)
                atom.calculate_transitions()

        intrinsic_times.append(global_time.current_time)
        for particle in particles:
            particle.update_state(global_time.dt, global_time)
            particle.calculate_dilated_time(global_time.dt, global_time)

        # Return a tuple of results
    return cesium_atoms, intrinsic_times, global_time.time_flow_rates, [p.dilated_times for p in particles]

# Plotting functions as defined in Code 1

def plot_transition_frequencies(cesium_atoms, with_ath=True):
    for i, atom in enumerate(cesium_atoms):
        transitions = list(atom.transition_frequencies.keys())
        frequencies = list(atom.transition_frequencies.values())

        plt.figure(figsize=(10, 6))
        plt.bar(range(len(transitions)), frequencies, tick_label=[f'{t[0]} to {t[1]}' for t in transitions])
        plt.xlabel('Transition')
        plt.ylabel('Frequency (Hz)')
        title = f"Cesium Atom {i+1} Transition Frequencies {'with' if with_ath else 'without'} ATH"
        plt.title(title)
        plt.yscale('log')  # Use log scale due to high frequency values
        plt.show()

def print_transition_frequencies(cesium_atoms, scenario):
    print(f"Transition Frequencies {scenario}:")
    for i, atom in enumerate(cesium_atoms):
        print(f"Cesium Atom {i+1}:")
        for transition, frequency in atom.transition_frequencies.items():
            print(f"  Transition {transition}: {frequency:.6e} Hz")
            

def plot_intrinsic_time_accumulation(intrinsic_times_with, intrinsic_times_without):
    plt.figure(figsize=(12, 6))
    plt.plot(intrinsic_times_with, label='With Active Time')
    plt.plot(intrinsic_times_without, label='Without Active Time', linestyle='--')
    plt.xlabel('Iteration')
    plt.ylabel('Accumulated Intrinsic Time')
    plt.title('Accumulation of Intrinsic Time Over Iterations')
    plt.legend()
    plt.show()

def plot_classical_vs_ath_time_evolution(intrinsic_times_with, intrinsic_times_without):
    plt.figure(figsize=(12, 6))
    plt.plot(intrinsic_times_with, label='With ATH')
    plt.plot(intrinsic_times_without, label='Classical (Without ATH)', linestyle='--')
    plt.title('Comparative Time Evolution: Classical vs. ATH')
    plt.xlabel('Iteration')
    plt.ylabel('Intrinsic Time')
    plt.legend()
    plt.show()

def plot_time_dilation_comparison(dilated_times_with, dilated_times_without):
    plt.figure(figsize=(12, 6))
    # Assuming dilated_times_with and dilated_times_without contain lists of dilated times for each simulation step
    average_dilated_time_with = np.mean([np.mean(times) for times in dilated_times_with])
    average_dilated_time_without = np.mean([np.mean(times) for times in dilated_times_without])
    
    plt.bar(['With ATH', 'Without ATH'], [average_dilated_time_with, average_dilated_time_without], color=['blue', 'orange'])
    plt.ylabel('Average Dilated Time')
    plt.title('Average Time Dilation: With ATH vs. Without ATH')
    plt.show()

def print_average_time_dilation(dilated_times, scenario):
    # Assuming dilated_times is a list of lists, where each inner list contains dilated times for a single particle
    all_dilated_times = [time for particle_times in dilated_times for time in particle_times]
    average_dilation = np.mean(all_dilated_times)
    print(f"Average Time Dilation {scenario}: {average_dilation:.6f}")  # Adjusted to show six decimal places



# Run the simulation for both scenarios
results_with_ath = run_simulation(use_active_time=True, max_iterations=1000)
results_without_ath = run_simulation(use_active_time=False, max_iterations=1000)

# Extracting results for scenarios with ATH
cesium_atoms_with_ath, intrinsic_times_with_ath, _, dilated_times_with_ath = results_with_ath

# Extracting results for scenarios without ATH
cesium_atoms_without_ath, intrinsic_times_without_ath, _, dilated_times_without_ath = results_without_ath

# Ensure transitions are calculated for both scenarios
for atom in cesium_atoms_with_ath + cesium_atoms_without_ath:
    atom.calculate_transitions()  # This ensures transition_frequencies is always set

# Now, print transition frequencies for both scenarios
print("\nTransition Frequencies with ATH:")
print_transition_frequencies(cesium_atoms_with_ath, "with ATH")
print("\nTransition Frequencies without ATH:")
print_transition_frequencies(cesium_atoms_without_ath, "without ATH")


# Plot transition frequencies for cesium atoms with ATH
plot_transition_frequencies(cesium_atoms_with_ath, with_ath=True)

# Plot transition frequencies for cesium atoms without ATH
plot_transition_frequencies(cesium_atoms_without_ath, with_ath=False)

# Plotting intrinsic time accumulation and comparative time evolution
plot_intrinsic_time_accumulation(intrinsic_times_with_ath, intrinsic_times_without_ath)
plot_classical_vs_ath_time_evolution(intrinsic_times_with_ath, intrinsic_times_without_ath)

# Plotting time dilation comparison
plot_time_dilation_comparison(dilated_times_with_ath, dilated_times_without_ath)

# Print average time dilation for both scenarios with more precision
print_average_time_dilation(dilated_times_with_ath, "with ATH")
print_average_time_dilation(dilated_times_without_ath, "without ATH")
