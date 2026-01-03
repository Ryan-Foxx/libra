import Footer from "../Footer";
import Header from "../Header";
import Sidebar from "../Sidebar";

function MainLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <>
            <Header />
            <Sidebar />
            {children}
            <Footer />
        </>
    );
}

export default MainLayout;
