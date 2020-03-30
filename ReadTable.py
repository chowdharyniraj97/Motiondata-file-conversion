import pandas as pd
d = pd.read_html("https://hellnar.github.io/openings/Openings.html")

print(type(d))
fname = "openings.txt"
with open(fname, "w", encoding="utf-8") as f:
    f.write(str(d))


# for table in d:
#     f.write(str(table))
#     f.write("\n")
