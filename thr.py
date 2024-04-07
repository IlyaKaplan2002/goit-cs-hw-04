import threading
import time


class KeywordSearchThread(threading.Thread):
    def __init__(self, file, keywords, results):
        threading.Thread.__init__(self)
        self.file = file
        self.keywords = keywords
        self.results = results

    def run(self):
        found_keywords = []
        try:
            with open(self.file, "r") as f:
                content = f.read()

                for keyword in self.keywords:
                    if keyword in content:
                        found_keywords.append(keyword)
        except Exception as e:
            print(f"Error processing file {self.file}: {e}")
        self.results[self.file] = found_keywords


def search_files_with_threads(files, keywords):
    results = {}
    threads = []
    for file in files:
        thread = KeywordSearchThread(file, keywords, results)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    new_results = {}

    for file, keywords in results.items():
        for keyword in keywords:
            if keyword in new_results:
                new_results[keyword].append(file)
            else:
                new_results[keyword] = [file]

    return new_results


if __name__ == "__main__":
    files = ["files/file1.txt", "files/file2.txt", "files/file3.txt"]  # Example files
    keywords = ["може", "частота", "ігор"]  # Example keywords

    start_time = time.time()
    results = search_files_with_threads(files, keywords)
    end_time = time.time()

    print("Results:")
    for keyword, found_files in results.items():
        print(f"Keyword: {keyword}, Files: {found_files}")

    print("Execution time:", end_time - start_time)
