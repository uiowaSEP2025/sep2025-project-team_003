export default interface JobSimplified {
    id: number;
    description: string;
    job_status: string;
    start_date: string | null;
    end_date: string | null;
    customer_name: string;
  }