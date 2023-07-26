export function Header() {
    return (
        <nav className="bg-gray-800 p-4">
            <div className="container mx-auto">
                <div className="flex items-center justify-between">
                <div className="text-white font-bold text-xl">Transcription Database</div>
                <ul className="flex space-x-4">
                    <li>
                    <a href="#" className="text-white hover:text-gray-300">Home</a>
                    </li>
                    <li>
                    <a href="#" className="text-white hover:text-gray-300">About</a>
                    </li>
                    <li>
                    <a href="#" className="text-white hover:text-gray-300">Contact</a>
                    </li>
                </ul>
                </div>
            </div>
        </nav>
    )
}
