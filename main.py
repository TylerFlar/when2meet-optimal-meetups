import csv
import time
import random
import argparse


def schedule_meetings(filename, interval=4, usernames=None):
    with open(filename, "r") as file:
        reader = csv.reader(file)
        header = next(reader)
        availability = list(reader)

    people = [person for person in header[1:] if not usernames or person in usernames]
    times = [row[0] for row in availability]
    parsed_times = [
        time.strptime(time_string, "%A %I:%M:%S %p") for time_string in times
    ]

    availability_dict = {}

    def is_next_time_valid(current_time, next_time):
        return (
            next_time.tm_hour == current_time.tm_hour
            and next_time.tm_min == current_time.tm_min + 15
        ) or (
            next_time.tm_hour == current_time.tm_hour + 1
            and next_time.tm_min == 0
            and current_time.tm_min == 45
        )

    for time_idx, current_time in enumerate(parsed_times):
        availability_dict[current_time] = []
        for person_idx, person in enumerate(people):
            is_available = True
            for i in range(interval):
                next_time_idx = time_idx + i
                if (
                    next_time_idx < len(parsed_times) - interval
                    and availability[time_idx + i][person_idx + 1] == "1"
                    and (
                        i == 0
                        or is_next_time_valid(
                            parsed_times[next_time_idx - 1], parsed_times[next_time_idx]
                        )
                    )
                ):
                    continue
                else:
                    is_available = False
                    break
            if is_available:
                availability_dict[parsed_times[time_idx]].append(person)

    availability_dict = dict(
        sorted(availability_dict.items(), key=lambda item: len(item[1]), reverse=True)
    )

    scheduled_people = []
    scheduled_times = []

    scheduled_times.append(list(availability_dict.keys())[0])
    for person in list(availability_dict.values())[0]:
        scheduled_people.append(person)

    every_person_scheduled = False

    while not every_person_scheduled:
        best_time_with_most_non_sched_people = 0
        best_time_with_most_non_sched_people_idx = -1
        for time_idx, (current_time, people) in enumerate(availability_dict.items()):
            if current_time not in scheduled_times:
                new_people = 0
                for person in people:
                    if person not in scheduled_people:
                        new_people += 1

                if new_people > best_time_with_most_non_sched_people:
                    best_time_with_most_non_sched_people = new_people
                    best_time_with_most_non_sched_people_idx = time_idx

        if best_time_with_most_non_sched_people_idx == -1:
            break

        scheduled_times.append(
            list(availability_dict.keys())[best_time_with_most_non_sched_people_idx]
        )
        for person in list(availability_dict.values())[
            best_time_with_most_non_sched_people_idx
        ]:
            if person not in scheduled_people:
                scheduled_people.append(person)

        for person in people:
            if person not in scheduled_people:
                every_person_scheduled = False
                break
            every_person_scheduled = True

    time_people = []
    for sched_time in scheduled_times:
        time_people.append((sched_time, availability_dict[sched_time]))

    return time_people


def format_output(time_people_list):
    days = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]

    formatted_list = []
    for time_struct, people in time_people_list:
        hour = time_struct.tm_hour % 12
        hour = 12 if hour == 0 else hour
        period = "AM" if time_struct.tm_hour < 12 else "PM"

        day = days[time_struct.tm_wday]

        formatted_time = f"{day}, {hour}:{str(time_struct.tm_min).zfill(2)} {period}"
        formatted_list.append((formatted_time, people))

    return formatted_list


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Schedule meetings based on availability."
    )
    parser.add_argument(
        "filename", type=str, help="CSV file containing availability data."
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=4,
        help="Number of consecutive 15-minute intervals.",
    )
    parser.add_argument(
        "--usernames", nargs="*", help="List of usernames to consider for scheduling."
    )

    args = parser.parse_args()

    # Pass usernames to the schedule_meetings function
    time_people = schedule_meetings(args.filename, args.interval, args.usernames)

    formatted_list = format_output(time_people)
    for time, people in formatted_list:
        print(f"{time}: {people}")
