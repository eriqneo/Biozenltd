// Business details in one place. Replace placeholders before launch.
export const site = {
  /** Registered business name: footer, copyright, page titles. */
  name: 'Biozen K Limited',
  /** Short brand name: logo and conversational copy. */
  shortName: 'Biozen',
  tagline: 'Medical equipment for clinics, hospitals and home care',
  url: 'https://www.example.com', // TODO: real domain
  // One primary contact number (Maesio's three numbers confused users).
  phone: '0791 384 788',
  phoneIntl: '+254791384788',
  whatsapp: '254791384788', // digits only, used in wa.me links
  email: 'sales@example.com', // TODO
  location: 'Nairobi, Kenya',
  freeDeliveryThreshold: 10000,
  /** Products above this KES price are steered to a quote rather than checkout. */
  quoteThreshold: 300000,
};

export const whatsappLink = (text: string) =>
  `https://wa.me/${site.whatsapp}?text=${encodeURIComponent(text)}`;

export const mainNav = [
  { label: 'Shop', href: '/shop' },
  { label: 'Offers', href: '/offers' },
  { label: 'Shop by Need', href: '/shop-by-need' },
  { label: 'For Clinics', href: '/clinics' },
  { label: 'Services', href: '/services' },
  { label: 'Guides', href: '/guides' },
];

export const footerNav = {
  Help: [
    { label: 'Delivery', href: '/help/delivery' },
    { label: 'Payments', href: '/help/payments' },
    { label: 'Returns', href: '/help/returns' },
    { label: 'FAQ', href: '/help/faq' },
  ],
  Services: [
    { label: 'Installation & training', href: '/services/installation' },
    { label: 'Maintenance & repairs', href: '/services/maintenance' },
    { label: 'Warranty', href: '/services/warranty' },
    { label: 'Request a quote', href: '/clinics/quote' },
  ],
  Company: [
    { label: 'About', href: '/about' },
    { label: 'Contact', href: '/contact' },
    { label: 'Careers', href: '/careers' },
    { label: 'Guides', href: '/guides' },
  ],
  Legal: [
    { label: 'Privacy', href: '/privacy' },
    { label: 'Terms', href: '/terms' },
    { label: 'Cookies', href: '/cookies' },
  ],
};
