import { Header } from "../Header/Header";
import { Search } from "../Search/Search";
import { Footer } from "../Footer/Footer";
export function DefaultContent() {
  return (
    <div>
      <Header />
      <div className="min-h-screen bg-gray-900">
        <div className="flex items-center justify-center">
          <h1 className="text-5xl font-bold mb-4 text-white text-center my-10">
            Title
          </h1>
        </div>
        <div className="container mx-auto">
          <div className="mb-4">
            <Search />
          </div>
          <div className="flex items-center justify-between"></div>
        </div>
      </div>
      <Footer />
    </div>
  );
}
