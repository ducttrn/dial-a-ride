import csv

if __name__ == "__main__":
    dfs_backtrack_sums = {}
    dfs_normal_sums = {}
    instances_count = {}

    with open('simulation-data.csv', 'r') as f:
        reader = csv.reader(f)
        data = list(reader)  # list(reader)[1:] to skip header
        for row in data:
            dfs_backtrack_sums[row[1]] = dfs_backtrack_sums.get(row[1], 0) + int(row[4])
            dfs_normal_sums[row[1]] = dfs_normal_sums.get(row[1], 0) + int(row[5])
            instances_count[row[1]] = instances_count.get(row[1], 0) + 1

    with open('simulation-data-aggregated.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(['requests_count', 'dfs_backtrack', 'dfs_normal'])
        for key in instances_count:
            writer.writerow([
                key,
                dfs_backtrack_sums[key] / instances_count[key],
                dfs_normal_sums[key] / instances_count[key]
            ])
