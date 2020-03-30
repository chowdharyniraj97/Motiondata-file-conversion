import pandas as pd
d = pd.read_html("https://hellnar.github.io/openings/Openings.html")

print(type(d))
df = d[0]
print(len(d))
print(df)
