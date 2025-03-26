import { JobDisplayInterface } from "./job.api.display.interface"
import { JobGeneralDataInterface } from "./job.api.general.data.interface"

export interface JobDataInterface {
    data: JobGeneralDataInterface,
    services: JobDisplayInterface,
    materials: JobDisplayInterface,
    contractors: JobDisplayInterface
}