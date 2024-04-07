import multiprocessing
import time


def search_files(file, keywords, results_queue):
    found_keywords = []

    try:
        with open(file, "r") as f:
            content = f.read()
            for keyword in keywords:
                if keyword in content:
                    found_keywords.append(keyword)
    except Exception as e:
        print(f"Error processing file {file}: {e}")
    results_queue.put({file: found_keywords})


def search_files_with_processes(files, keywords):
    manager = multiprocessing.Manager()
    results_queue = manager.Queue()
    processes = []
    for file in files:
        process = multiprocessing.Process(
            target=search_files,
            args=(file, keywords, results_queue),
        )
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    results = {}
    while not results_queue.empty():
        results.update(results_queue.get())

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
    results = search_files_with_processes(files, keywords)
    end_time = time.time()

    print("Results:")
    for keyword, found_files in results.items():
        print(f"Keyword: {keyword}, Files: {found_files}")

    print("Execution time:", end_time - start_time)
