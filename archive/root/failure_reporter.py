from failure_categorizer import categorize_error, update_grind_log, update_learned_lessons, count_errors_by_category

def report_failure(error):
    error_category = categorize_error(error)
    grind_log = {"error": error}
    updated_grind_log = update_grind_log(grind_log, error_category)
    print(updated_grind_log)

    learned_lessons = {}
    updated_learned_lessons = update_learned_lessons(learned_lessons, error_category)
    print(updated_learned_lessons)

    error_counts = count_errors_by_category(updated_learned_lessons)
    print(error_counts)

def main():
    # Example usage:
    error = "Timeout occurred during grind session"
    report_failure(error)

if __name__ == "__main__":
    main()