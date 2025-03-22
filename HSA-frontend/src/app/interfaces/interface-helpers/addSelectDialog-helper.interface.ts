import { InputFieldDictionary } from "./inputField-row-helper.interface";

export interface AddSelectDialogData {
    typeOfDialog: string,
    dialogData: any,
    searchHint: string;
    headers: string[]
    materialInputFields: InputFieldDictionary[]
}