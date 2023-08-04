import { Search } from "../Search/Search";
import { useLocation } from "react-router-dom";
import { SearchResultCards } from "./SearchResultCards";
import { Header } from "../Header/Header";
import { Footer } from "../Footer/Footer";

const SearchResultPage = () => {
  const location = useLocation();
  const searchData = location.state.data; // Access the search result data from location state

  return (
    <div className="min-h-screen bg-gray-900">
      <Header />
      <div className="flex flex-col items-center justify-center">
        <h1 className="text-5xl font-bold mb-4 text-white text-center my-10">
          Search Your Transcripts
        </h1>
        <div className="container mx-auto">
          <div className="flex grid justify-center items-center bg-gray-900">
            <div className="mb-4">
              <Search />
              <div className="mb-4"></div>
              <SearchResultCards searchData={searchData} />
            </div>
          </div>
        </div>
      </div>
      <Footer />
    </div>
  );
};

export default SearchResultPage;
