# NPR: Detail-Preserving Non-Photorealistic Rendering

## 📖 About The Project

**NPR** is a high fidelity Non-Photorealistic Rendering (NPR) web application. This project operates within the specialized subfield of computer vision focused on programmatically transforming standard RGB photographs into stylized artworks specifically graphite pencil sketches and watercolor illustrations.

Instead of relying on opaque, pre-packaged library functions (like basic OpenCV filters) or computationally heavy deep learning models (CNNs/GANs), we engineered a custom, deterministic mathematical pipeline. Our approach uses fundamental pixel manipulation techniques to ensure precise developer control, structural edge preservation, and instant CPU-bound execution.

### Key Features

  * **Custom Mathematical Pipelines:** Hand-crafted algorithms for tonal shading, color pooling, and ink-outline extraction.
  * **Detail-Preserving Synthetics:** Utilizes alpha-blending and Contrast Limited Adaptive Histogram Equalization (CLAHE) to preserve the semantic integrity of the original photo.
  * **Interactive UI:** A vibrant, dark-mode frontend featuring drag-and-drop uploads and asynchronous processing.
  * **Side-by-Side Analysis:** Instantly compare the original photograph with the stylized algorithmic output in a responsive grid.
  * **CPU-Optimized:** Runs instantly on standard hardware without the need for a dedicated GPU.

-----

## 🛠️ Built With

  * **Backend:** Python 3.x, Flask, Werkzeug
  * **Computer Vision:** OpenCV (`cv2`), NumPy
  * **Frontend:** HTML5, CSS3, Vanilla JavaScript (ES6+), Fetch API

-----

## 🧠 Algorithmic Architecture

We divided our processing logic into two highly specialized pipelines:

### 1\. Professional Pencil Sketch Pipeline

Inspired by traditional darkroom "Color Dodging" techniques, this pipeline simulates graphite on paper:

  * **Contrast Enhancement:** Flattens the image to grayscale and applies CLAHE to deepen shadows and brighten highlights.
  * **Multi-Scale Shading:** Inverts the image and applies both fine and broad Gaussian blurs to simulate varying pressures of a physical graphite smudge.
  * **Structural Overlay:** Utilizes a hybrid Laplacian and Canny Edge detection approach, thickened via matrix dilation, to capture stark outlines and fine internal textures.

### 2\. Balanced Watercolor Pipeline

Designed to simulate wet paint and ink outlines without degrading into unrecognizable noise:

  * **Edge-Preserving Smoothing:** Utilizes Bilateral Filtering to flatten textures into "painted" pools of color while strictly halting at high-contrast edges.
  * **Pigment Saturation:** Shifts to the HSV color space to mathematically boost the saturation channel, mimicking vivid watercolor pigments.
  * **Recombination:** Inverts structural Canny edges to act as "ink outlines" and blends them over the painted color pools using the alpha-blending formula:
    $I_{final} = (I_{stylized} \cdot \alpha) + (I_{original} \cdot (1 - \alpha))$

-----

## 🚀 Getting Started

Follow these instructions to get a local copy of the project up and running on your machine.

### Prerequisites

Make sure you have Python 3.8+ installed on your system.

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/THEELITE100/ACV.git
    cd ACV
    ```

2.  **Create a virtual environment (Recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install the required dependencies:**

    ```bash
    pip install Flask opencv-python numpy werkzeug
    ```

4.  **Verify Directory Structure:**
    Ensure the following empty directories exist to handle file processing:

    ```bash
    mkdir -p static/uploads
    mkdir -p static/outputs
    ```

### Running the Application

1.  Start the Flask development server:
    ```bash
    python app.py
    ```
2.  Open your web browser and navigate to: `http://127.0.0.1:5000`

-----

## 👥 Meet the Team

  * **Sumit:** Research, Literature Review, and Server Routing Architecture (Flask Backend).
  * **Rohan:** Computer Vision Engineering (Pencil Sketch Algorithm & Edge Overlay).
  * **Anurag:** Computer Vision Engineering (Watercolor Algorithm & Detail Preservation).
  * **Akshat:** Compilation, Frontend UI Design, and Asynchronous JavaScript Integration.

-----

## 📚 References & Acknowledgments

Our methodologies were heavily inspired by the foundational mathematics found in the following literature:

  * Lu, C., Xu, L., & Jia, J. (2012). *Combining Sketch and Tone for Pencil Drawing Production*.
  * Canny, J. (1986). *A Computational Approach to Edge Detection*.
  * Tomasi, C., & Manduchi, R. (1998). *Bilateral Filtering for Gray and Color Images*.