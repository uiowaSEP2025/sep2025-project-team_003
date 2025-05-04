export default function parseTimeToDate(timeStr: string, baseDate: Date = new Date()): Date {
    const [time, modifier] = timeStr.split(' ');
    let [hours, minutes] = time.split(':').map(Number);
  
    if (modifier === 'PM' && hours < 12) hours += 12;
    if (modifier === 'AM' && hours === 12) hours = 0;
  
    const date = new Date(baseDate);
    date.setHours(hours, minutes, 0, 0);
    return date;
  }