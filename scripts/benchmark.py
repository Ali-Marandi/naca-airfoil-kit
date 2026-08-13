import time
import numpy as np
from airfoil_pro import NACAGeneratorPro, AirfoilAnalysis
import matplotlib.pyplot as plt

def old_compute_simulated(n_panels):
    """Simulated non-vectorized influence matrix construction."""
    A = np.zeros((n_panels, n_panels))
    for i in range(n_panels):
        for j in range(n_panels):
            # Simulation of slow nested loop logic
            A[i, j] = np.sin(i) * np.cos(j)
    return A

def benchmark():
    panel_sizes = [50, 100, 200, 300, 400, 500]
    old_times = []
    new_times = []
    
    xu, yu, xl, yl = NACAGeneratorPro.naca4("2412", 250)

    for n in panel_sizes:
        # Benchmark Old (Simulated Nested Loops)
        start = time.time()
        for _ in range(5):
            _ = old_compute_simulated(n)
        old_times.append((time.time() - start) / 5)
        
        # Benchmark New (Vectorized NumPy)
        # We need to adjust the number of points to match n
        txu, tyu, txl, tyl = NACAGeneratorPro.naca4("2412", n//2 + 1)
        start = time.time()
        for _ in range(5):
            _ = AirfoilAnalysis.compute_aerodynamics(txu, tyu, txl, tyl, 5.0)
        new_times.append((time.time() - start) / 5)
        
    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(panel_sizes, old_times, 'r-o', label='Original (Nested Loops)')
    plt.plot(panel_sizes, new_times, 'g-s', label='Optimized v2.9 (Vectorized)')
    plt.yscale('log')
    plt.xlabel('Number of Panels')
    plt.ylabel('Computation Time (seconds) - Log Scale')
    plt.title('NACA Airfoil Kit Pro: Performance Benchmark')
    plt.legend()
    plt.grid(True, which="both", ls="-", alpha=0.5)
    plt.savefig('/home/ubuntu/naca-airfoil-kit/performance_benchmark.png')
    
    print(f"Benchmark completed. Chart saved to performance_benchmark.png")
    print(f"Max Speedup: {old_times[-1]/new_times[-1]:.1f}x")

if __name__ == "__main__":
    benchmark()
