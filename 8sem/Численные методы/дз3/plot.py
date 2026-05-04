import matplotlib.pyplot as plt
import numpy as np

def graphic(x_function, y_function, x_points, y_points, xlim, ylim, n_point, name_function, method = 0, df = 0, function = 0, type = 0, n_cas = 0, color = 'white', xaxis=False, up=False):
    
    if color == 'black':
        plt.rcParams['axes.facecolor'] = "#1f1f1f"    
        plt.rcParams['figure.facecolor'] = "#1f1f1f"      
        plt.rcParams['grid.color'] = '#777777'         
        plt.rcParams['grid.linestyle'] = '--'         
        plt.rcParams['grid.linewidth'] = 0.5            
        plt.rcParams['grid.alpha'] = 0.8
        plt.rcParams['font.size'] = 16                 
        plt.rcParams['xtick.color'] = '#aaaaaa'     
        plt.rcParams['ytick.color'] = '#aaaaaa'         
        plt.rcParams['axes.labelcolor'] = '#aaaaaa'    
        plt.rcParams['axes.titlecolor'] = '#aaaaaa'
        plt.rcParams['legend.labelcolor'] = '#aaaaaa'  
    else:
        plt.rcdefaults()

    plt.figure(figsize=(22, 5))
    plt.xlim(xlim)
    plt.ylim(ylim)
    plt.plot(x_function,y_function, linewidth=3, label=name_function, zorder=0)
    plt.legend(fontsize=20)
    plt.xlabel('x', fontsize=20)
    plt.scatter(x_points, y_points, c="#c586c0", s=30, alpha=0.8, zorder=2)
    plt.scatter(x_points[len(x_points)-1], y_points[len(x_points)-1], c="#BD481A", s=30, zorder=2)
    plt.grid(alpha=0.4)
    for i, (xi, yi, label) in enumerate(zip(x_points, y_points, np.arange(0, len(x_points), 1))):
        if i < n_point:
            plt.annotate(label, (xi, yi), 
                        xytext=(-4, -20) if not(up) else (-4, 5),  
                        textcoords='offset points',
                        fontsize=14,
                        fontweight='bold', color=('#aaaaaa' if color == 'black' else "#666666FF"))
            
    if method == 'nuton':
        for i in range(n_cas):
            x = np.array([x_points[i+1]-0.01, x_points[i]+0.03])
            y = function(type, x_points[i]) + (x - x_points[i])*df[i]
            plt.plot(x,y, c=('#aaaaaa' if color == 'black' else "#666666FF"),zorder=1, linewidth=2)
            plt.plot([x_points[i]]*2, [0,function(type, x_points[i])], '--', c=('#aaaaaa' if color == 'black' else "#666666FF"), linewidth=2)
            plt.scatter(x_points[i], function(type, x_points[i]), c="#664263", s=20, alpha=0.8, zorder=3)

    if method == 'secant':
        plt.plot([x_points[0]]*2, [0,function(type, x_points[0])], '--', c=('#aaaaaa' if color == 'black' else "#666666FF"), linewidth=2)
        plt.scatter(x_points[0], function(type, x_points[0]), c="#664263", s=20, alpha=0.8, zorder=3)
        for i in range(n_cas):
            x = np.array([x_points[i+2], x_points[i+1], x_points[i]])
            y = np.array([0, function(type, x_points[i+1]),function(type, x_points[i])])
            plt.plot(x,y, c=('#aaaaaa' if color == 'black' else "#666666FF"),zorder=1, linewidth=2)
            plt.plot([x_points[i+1]]*2, [0,function(type, x_points[i+1])], '--', c=('#aaaaaa' if color == 'black' else "#666666FF"), linewidth=2)
            plt.scatter(x_points[i+1], function(type, x_points[i+1]), c="#664263", s=20, alpha=0.8, zorder=3)
    if xaxis:
        plt.plot(x_function, [0]*len(x_function), c=('#aaaaaa' if color == 'black' else "#995C91FF"), linewidth=1,zorder=-1)