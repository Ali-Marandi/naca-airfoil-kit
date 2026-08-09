from airfoil_pro import NACAGeneratorPro, AirfoilAnalysis, GeometryOptimizer, UIUCLoader

def naca4(code, points=100):
    res = NACAGeneratorPro.naca4(code, n_points=points)
    if res:
        xu, yu, xl, yl = res
        return list(zip(xu, yu)), list(zip(xl, yl))
    return None, None
