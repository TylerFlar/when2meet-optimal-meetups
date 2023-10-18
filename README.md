# When2Meet Optimal Meetups

## Description

When2Meet Optimal Meetup is a Python script that uses a CSV generated from When2Meet to determine the best meeting times for a group. It schedules meetings based on the number of consecutive 15-minute intervals where the most people ar available resulting in a list of most optimal weekly meeting times to get everyone on the When2Meet.

## Requirements
* Python 3.x
* A CSV file from When2Meet

## Usage
Interval specifies the number of 15 minute periods. Four is one hour. Default interval is `4`.

```python main.py when2meet.csv --interval 4```

## CSV from When2Meet
Paste this script into the Chrome console tab on the When2Meet page.

```js
function getCSV() {
  result = "Time," + PeopleNames.join(",")+"\n"; 
  for(let i = 0; i < AvailableAtSlot.length; i++) {
      let slot = $x(`string(//div[@id="GroupTime${TimeOfSlot[i]}"]/@onmouseover)`);
      slot = slot.match(/.*"(.*)".*/)[1];
      result += slot + ",";
      result += PeopleIDs.map(id => AvailableAtSlot[i].includes(id) ? 1 : 0).join(",");
      result+= "\n";
  }
  console.log(result);
  return result;
}

content = getCSV()

const link = document.createElement("a");

const file = new Blob([content], { type: 'text/plain' });

link.href = URL.createObjectURL(file);

link.download = "when2meet.csv";

link.click();
URL.revokeObjectURL(link.href);
```

Taken from: https://gist.github.com/camtheman256/3125e18ba20e90b6252678714e5102fd