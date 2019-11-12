"""
Plot Interactive Polar Bar Evolution Example.
==================================
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
from templot import plot_polar_bar_evolution, add_regions, download_irep


filepath = os.path.join('..', 'templot', 'data', 'df.csv')

if not os.path.exists(filepath):
    download_irep(filepath)
    df = pd.read_csv(filepath)
    df = add_regions(df, "LLX", "LLY")
    df.to_csv(filepath, index=False)

df = pd.read_csv(filepath)


df = pd.melt(
    df,
    id_vars=['Identifiant', 'Nom_Etablissement_x', 'LLX', 'LLY', 'Regions'],
    var_name='Annee',
    value_name='Quantite',
)
df = df[df.Quantit != 0]
df['Annee'] = df['Annee'].apply(lambda x: x[-4:])
plot = plot_polar_bar_evolution_interactive(df)
plt.show()

# visualize the html results in sphinx gallery
tmp_dir = os.path.join('..', 'dist', 'html')
if os.path.exists(tmp_dir):
    pass


####################################
# .. raw:: html
#
#     <iframe src="../example_polarbar.html" height="620px" width="100%"></iframe>
