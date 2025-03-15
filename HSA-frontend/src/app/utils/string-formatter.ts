import { Injectable } from "@angular/core";

@Injectable({
  providedIn: 'root'
})
export class StringFormatter {
    formatSnakeToCamel(snakeCase: string): string {
        return snakeCase.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');
    }
    
    formatCamelToSnake(camelCase: string): string {
      return camelCase.split(' ').map(word => word.toLowerCase()).join('_');
    }

    formatJSONData(element: Record<string, any>): string {
      const entries = Object.entries(element);
    
      const [idKey, idValue] = entries.find(([key]) => key.toLowerCase().includes('id')) || ["Unknown ID", "N/A"];
      const [dataKey, dataValue] = entries.find(([key]) => key !== idKey) || ["Unknown Field", "N/A"];
    
      return `${this.formatSnakeToCamel(dataKey).replace(/_/g, ' ')}: ${dataValue} (${this.formatSnakeToCamel(idKey)}: ${idValue})`;
    }

    formatCurrency(amount: string): string {
      return `$${parseFloat(amount).toFixed(2)}`
    }
}