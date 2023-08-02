// Define the data for the cards
import lectureImage from "../../assets/thumbnails/lectures/Lecture 1_ Course Overview + The Shell (2020).jpg";

export interface Card {
  title: string;
  image: string;
  description: string;
}

export const cardData: Card[] = [
  {
    title: "Lecture 3: Editors (vim) (2020)",
    image: lectureImage,
    description: "test",
  },
  {
    title: "Lecture 1: Course Overview + The Shell (2020)",
    image:
      "https://drive.google.com/uc?export=view&id=1vGhiQ9cSG1e9c4uYXp6SwC71VrZHeWUE",
    description: "Lecture 1: Course Overview + The Shell (2020)",
  },
  {
    title: "Lecture 2: Shell Tools and Scripting (2020)",
    image:
      "https://drive.google.com/uc?export=view&id=1cDYbLFZIfQkPA5qVrmTyAEmxzJbIKVhB",
    description: "Lecture 2: Shell Tools and Scripting (2020)",
  },
  {
    title: "Lecture 3: Editors (vim) (2020)",
    image:
      "https://drive.google.com/uc?export=view&id=1qUNqRMsEJqF97OZynh0meYRAdEQUXlir",
    description: "Lecture 3: Editors (vim) (2020)",
  },
  {
    title: "Lecture 4: Data Wrangling (2020)",
    image:
      "https://drive.google.com/uc?export=view&id=1S_mUX3oW7nQRgtPE1qx7OnuV5P9gU8Mo",
    description: "Lecture 4: Data Wrangling (2020)",
  },
  {
    title: "Lecture 5: Command-line Environment (2020)",
    image:
      "https://drive.google.com/uc?export=view&id=1Ku9GTVroATHFPEs6xfybMUEHGk-cc22x",
    description: "Lecture 5: Command-line Environment (2020)",
  },
  {
    title: "Lecture 6: Version Control (git) (2020)",
    image:
      "https://drive.google.com/uc?export=view&id=19nk-ZjSVFQCJvB2lLSSnSwGi6RGxad_F",
    description: "Lecture 6: Version Control (git) (2020)",
  },
  {
    title: "Lecture 7: Debugging and Profiling (2020)",
    image:
      "https://drive.google.com/uc?export=view&id=1ACvCaDTSggvOTR83pkOqBrt54ptrjnUy",
    description: "Lecture 7: Debugging and Profiling (2020)",
  },
  {
    title: "Lecture 8: Metaprogramming (2020)",
    image:
      "https://drive.google.com/uc?export=view&id=1Gm8vFcTkuGX0mf1vOP4yzt8mw6TGD0fg",
    description: "Lecture 8: Metaprogramming (2020)",
  },
  {
    title: "Lecture 9: Security and Cryptography (2020)",
    image:
      "https://drive.google.com/uc?export=view&id=1qieMWNFKch9quIO-v7HXEGzN3jPDOIKN",
    description: "Lecture 9: Security and Cryptography (2020)",
  },
  {
    title: "Lecture 10: Potpourri (2020)",
    image:
      "https://drive.google.com/uc?export=view&id=1KsW31_i99Fp5kx8BdlMFV-WPm8QcSfL_",
    description: "Lecture 10: Potpourri (2020)",
  },
  {
    title: "Lecture 11: Q&A (2020)",
    image:
      "https://drive.google.com/uc?export=view&id=1-ffZiAvNlWc4nYCvWHGpYv_4xw6PhWD5",
    description: "Lecture 11: Q&A (2020)",
  },
  // Add more card data as needed
];
