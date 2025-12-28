import type { Metadata } from "next";
import "@/styles/main.css";

export const metadata: Metadata = {
    title: "خرید و دانلود کتاب الکترونیکی و کتاب صوتی با لیبرا",
    description:
        "کتاب الکترونیک و کتاب صوتی را در لیبرا بخوانید. | دانلود و خرید انواع کتاب متنی و صوتی با بهترین قیمت و کیفیت | لیبرا؛ دسترسی به هزاران کتاب، رمان و مجله",
};

export default function RootLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <html lang="en">
            <body>{children}</body>
        </html>
    );
}
