import asyncio
import re
from collections import Counter

import aiofiles
import matplotlib.pyplot as plt


class LogVisualizer:
    def __init__(self, log_file):
        self.log_file = log_file
        self.logs = []
        self.filtered_logs = []
        print(f"Initialized LogVisualizer with file: {log_file}")

    async def load_logs(self):
        """Load logs from the file."""
        try:
            async with aiofiles.open(self.log_file, 'r') as file:
                self.logs = await file.readlines()
            self.filtered_logs = self.logs[:]
            print(f"Loaded {len(self.logs)} logs from {self.log_file}")
        except FileNotFoundError:
            print(f"File {self.log_file} not found.")

    async def filter_logs(self, keyword):
        """Filter logs based on a keyword."""
        print(f"Filtering logs with keyword: {keyword}")
        self.filtered_logs = [log for log in self.logs if keyword in log]
        print(f"Filtered {len(self.filtered_logs)} logs out of {len(self.logs)}")

    async def group_logs(self, pattern):
        """Group logs by a regex pattern."""
        print(f"Grouping logs with pattern: {pattern}")
        grouped = {}
        regex = re.compile(pattern)
        for log in self.filtered_logs:
            match = regex.search(log)
            if match:
                key = match.group(0)
                grouped.setdefault(key, []).append(log)
        print(f"Grouped logs into {len(grouped)} groups")
        return grouped

    async def show_statistics(self):
        """Show statistics of log occurrences by hour."""
        print("Generating statistics...")
        timestamps = []
        for log in self.filtered_logs:
            match = re.search(r'\d{4}-\d{2}-\d{2} \d{2}', log)
            if match:
                timestamps.append(match.group(0))

        counter = Counter(timestamps)
        sorted_data = sorted(counter.items())
        print(f"Timestamps found: {len(sorted_data)}")

        if not sorted_data:
            print("No valid timestamps found. Cannot generate statistics.")
            return

        times, counts = zip(*sorted_data)

        plt.figure(figsize=(10, 5))
        plt.bar(times, counts, color='skyblue')
        plt.xlabel('Time (Hour)')
        plt.ylabel('Log Count')
        plt.title('Log Statistics by Hour')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    async def search_logs(self, query):
        """Search logs for a specific query."""
        print(f"Searching logs with query: {query}")
        results = [log for log in self.filtered_logs if query in log]
        print(f"Found {len(results)} matching logs")
        return results


async def main():
    log_file = input("Enter the path to the log file: ")
    print(f"Starting LogVisualizer with file: {log_file}")
    visualizer = LogVisualizer(log_file)

    await visualizer.load_logs()

    while True:
        print("\nOptions:")
        print("1. Filter logs by keyword")
        print("2. Group logs by pattern")
        print("3. Show statistics")
        print("4. Search logs")
        print("5. Exit")

        choice = input("Choose an option: ")
        print(f"Selected option: {choice}")

        if choice == "1":
            keyword = input("Enter keyword to filter: ")
            await visualizer.filter_logs(keyword)

        elif choice == "2":
            pattern = input("Enter regex pattern to group logs: ")
            grouped_logs = await visualizer.group_logs(pattern)
            for key, group in grouped_logs.items():
                print(f"\nGroup: {key}")
                for log in group:
                    print(log.strip())

        elif choice == "3":
            await visualizer.show_statistics()

        elif choice == "4":
            query = input("Enter search query: ")
            results = await visualizer.search_logs(query)
            for result in results:
                print(result.strip())

        elif choice == "5":
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    asyncio.run(main())
