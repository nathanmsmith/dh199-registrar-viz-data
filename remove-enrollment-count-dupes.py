import csv
import sys

# SELECT enrollment_data.section_id, enrollment_data.enrollment_count, AGE(enrollment_data.created_at, '02-10-2020Z08:00') FROM enrollment_data JOIN sections ON enrollment_data.section_id = sections.id WHERE term = '20S' ORDER BY enrollment_data.created_at;

file_name = sys.argv[1]

with open(f"{file_name}.csv", newline="") as file, open(
    f"{file_name}-deduped.csv", "w", newline=""
) as outfile:
    reader = csv.reader(file)
    writer = csv.writer(outfile)

    headers = next(reader, None)
    writer.writerow(headers)

    last_counts_for_section = {}

    for section_id, enrollment_count, created_at in reader:

        created_at = created_at.strip('"')

        row = [section_id, enrollment_count, created_at]

        if section_id in last_counts_for_section:
            last_enrollment_count = last_counts_for_section[section_id][1]
            if last_enrollment_count == enrollment_count:
                pass
            else:
                writer.writerow(row)
        else:
            writer.writerow(row)

        last_counts_for_section[section_id] = row

    # always write last row
    for section_id, row in last_counts_for_section.items():
        writer.writerow(row)
