import { Link } from "react-router-dom";

export function Header() {
  return (
    <nav className="bg-gray-800 p-4">
      <div className="container mx-auto">
        <div className="flex items-center justify-between">
          <Link to="/" className="text-white font-bold text-xl">
            Transcription Database
          </Link>
          <ul className="flex space-x-4">
            <li>
              <a
                href="https://github.com/christopher-luu97/TranscriptionSearch"
                className="text-white hover:text-gray-300"
              >
                GitHub
              </a>
            </li>
            <li>
              <a
                href="https://www.linkedin.com/in/christopher-luu-542691149"
                className="text-white hover:text-gray-300"
              >
                Social
              </a>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  );
}
