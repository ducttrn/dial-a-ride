import csv

if __name__ == "__main__":
    lcf_sum = {}
    dfs_sum = {}
    instances_count = {}

    with open('simulation-data.csv', 'r') as f:
        reader = csv.reader(f)
        data = list(reader)  # list(reader)[1:] to skip header
        for row in data:
            lcf_sum[row[1]] = lcf_sum.get(row[1], 0) + int(row[4])
            dfs_sum[row[1]] = dfs_sum.get(row[1], 0) + int(row[5])
            instances_count[row[1]] = instances_count.get(row[1], 0) + 1

    with open('simulation-data-aggregated.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(['requests_count', 'lcf', 'dfs'])
        for key in instances_count:
            writer.writerow([
                key,
                lcf_sum[key] / instances_count[key],
                dfs_sum[key] / instances_count[key]
            ])
