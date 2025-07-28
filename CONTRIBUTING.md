# Contribution Guidelines See, before start running the pipeline.

# Installation

1. Clone the repository:
   ```shell
   git clone <repo_ssh_address>
   ```
2. Switch to the project directory:
   ```shell
    cd <project_name>
    ```
3. Create a virtual environment.

   ```bash
    python  -m venv consultancy-assessment
    ```

4. Activate the virtual environment.


   ```bash
     source consultancy-assessment/Scripts/activate
    ```


2. Install the project in editable mode along with development dependencies:
    ```bash
    pip install -e ".[dev]"
    ```