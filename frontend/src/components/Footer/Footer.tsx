export function Footer() {
  return (
    <footer className="bg-gray-800 p-2">
      <div className="container mx-auto">
        <p className="text-white text-center">
          &copy; {new Date().getFullYear()} Christopher Luu. All rights
          reserved.
        </p>
      </div>
    </footer>
  );
}
