export interface MenuInterface {
  name: string;
  route: string;
  description: string;
}

export const MENU_ITEMS: MenuInterface[] = [
  {
    name: 'Jobs',
    route: "/jobs",
    description: "Manage your jobs"
  },
  {
    name: 'Requests',
    route: "/requests",
    description: "Manage your requests"
  },
  {
    name: 'Customers',
    route: "/customers",
    description: "Manage your customers"
  },
  {
    name: 'Services',
    route: "/services",
    description: "Manage your services"
  },
  {
    name: 'Materials',
    route: "/materials",
    description: "Manage your materials"
  },
  {
    name: 'Contractors',
    route: "/contractors",
    description: "Manage your contractors"
  },
  {
    name: 'Bookings',
    route: "/booking",
    description: "Manage your bookings"
  },
  {
    name: 'Invoices',
    route: "/invoices",
    description: "Manage your invoices"
  },
  {
    name: 'Quotes',
    route: "/quotes",
    description: "Manage your quotes"
  },

];
