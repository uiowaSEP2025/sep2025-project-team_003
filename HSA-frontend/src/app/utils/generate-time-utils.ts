export function generateTimes(isEnd: boolean, selectedDate: Date): Date[] {
  const times: Date[] = [];
  let currentTime = new Date(selectedDate);

  currentTime.setHours(0, 0, 0, 0);

  for (let i = 0; i < 96; i++) {
    times.push(new Date(currentTime));
    currentTime.setMinutes(currentTime.getMinutes() + 15);
  }
  if (isEnd) {
    times.shift();

    const lastTime = new Date(currentTime);
    lastTime.setHours(23, 59, 0, 0);
    times.push(lastTime);
  }

  return times;
}
