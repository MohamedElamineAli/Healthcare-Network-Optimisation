# Setting up the environment
This guide will help you set up an Anaconda environment using the `environment.yaml` file provided in this repository.

## Prerequisites

Before you begin, make sure you have Anaconda installed on your system. If not, you can download and install Anaconda from the [official Anaconda website](https://www.anaconda.com/download).

## Installation Steps
### Using Command Line (Anaconda Prompt)
1. **Clone the Repository:**

    Clone this repository to your local machine using the following command:
    
    ```bash
    git clone https://github.com/MohamedElamineAli/Healthcare-Network-Optimisation
    ```

2. **Navigate to the Repository Directory:**

    Use the `cd` command to navigate to the directory where you cloned the repository:
    
    ```bash
    cd Healthcare-Network-Optimisation
    ```

3. **Create Anaconda Environment:**

    Use the `conda env create` command to create a new Anaconda environment from the `environment.yaml` file:
    
    ```bash
    conda env create -f environment.yaml
    ```

4. **Activate the Environment:**

    Activate the newly created Anaconda environment using the following command:
    
    ```bash
    conda activate <environment-name>
    ```
### Using Anaconda Navigator (Graphical Interface)
1. **Launch Anaconda Navigator:**

    Open Anaconda Navigator from your system's application menu.

2. **Import Environment from YAML File:**

    - Click on the "Import" button under the "Environments" tab.
    - Browse and select the `environment.yaml` file from the cloned repository.
    - Click "Open" to import the environment.

3. **Activate the Environment:**
    - Once imported, find the newly created environment in the list.
    - Click on the environment name to activate it

## Additional Notes
- Remember to deactivate the environment when you're finished using it:
  
    ```bash
    conda deactivate
    ```

- For more information on managing Anaconda environments, refer to the [official Anaconda documentation](https://docs.anaconda.com/).

## Feedback and Contributions

If you encounter any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request on GitHub.
