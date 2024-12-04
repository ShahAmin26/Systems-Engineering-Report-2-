#Shah Amins python coding for chapter 5 (statistical analysis/uncertainty)

# monte_carlo_analysis.py

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns

class CDSSStatisticalAnalysis:
    def __init__(self):
        self.n_iterations = 10000
        self.results = {
            'accuracy': [],
            'response_time': [],
            'data_completeness': [],
            'symptom_clarity': [],
            'workflow_variation': []
        }

    def simulate_diagnostic_accuracy(self):
        """
        Monte Carlo simulation for diagnostic accuracy analysis
        Returns: Dictionary of simulation results
        """
        for _ in range(self.n_iterations):
            # Generate random parameters
            data_completeness = np.random.uniform(0.6, 1.0)
            symptom_clarity = np.random.randint(1, 6)
            workflow_variation = np.random.choice(range(8))
            response_time = np.random.exponential(scale=2.0)

            # Calculate accuracy based on parameters
            base_accuracy = 0.90  # Base accuracy of 90%
            accuracy = base_accuracy * data_completeness * \
                      (symptom_clarity/5) * \
                      (1 - workflow_variation*0.01) * \
                      (1 - min(response_time/10, 0.1))

            # Store results
            self.results['accuracy'].append(accuracy * 100)  # Convert to percentage
            self.results['response_time'].append(response_time)
            self.results['data_completeness'].append(data_completeness)
            self.results['symptom_clarity'].append(symptom_clarity)
            self.results['workflow_variation'].append(workflow_variation)

        return self.results

    def calculate_statistics(self):
        """
        Calculate key statistical measures
        """
        accuracy_array = np.array(self.results['accuracy'])
        return {
            'mean_accuracy': np.mean(accuracy_array),
            'std_accuracy': np.std(accuracy_array),
            'ci_95': stats.norm.interval(0.95, 
                                      loc=np.mean(accuracy_array),
                                      scale=stats.sem(accuracy_array)),
            'percentile_99_response': np.percentile(self.results['response_time'], 99)
        }

    def sensitivity_analysis(self):
        """
        Perform sensitivity analysis on input parameters
        """
        # Calculate correlation coefficients
        correlations = {
            'data_completeness': np.corrcoef(self.results['data_completeness'], 
                                           self.results['accuracy'])[0,1],
            'symptom_clarity': np.corrcoef(self.results['symptom_clarity'], 
                                         self.results['accuracy'])[0,1],
            'workflow_variation': np.corrcoef(self.results['workflow_variation'], 
                                            self.results['accuracy'])[0,1],
            'response_time': np.corrcoef(self.results['response_time'], 
                                       self.results['accuracy'])[0,1]
        }
        
        # Normalize to percentages
        total = sum(abs(val) for val in correlations.values())
        sensitivity = {key: abs(val)/total * 100 for key, val in correlations.items()}
        return sensitivity

    def plot_diagnostic_accuracy(self, save_path='figure11.png'):
        """
        Generate Figure 11: Distribution of Diagnostic Accuracy
        """
        plt.figure(figsize=(10, 6))
        sns.histplot(self.results['accuracy'], kde=True)
        plt.axvline(np.mean(self.results['accuracy']), color='g', linestyle='--')
        plt.axvline(self.calculate_statistics()['ci_95'][0], color='r', linestyle='--')
        plt.axvline(self.calculate_statistics()['ci_95'][1], color='r', linestyle='--')
        plt.title('Distribution of Diagnostic Accuracy')
        plt.xlabel('Accuracy (%)')
        plt.ylabel('Frequency')
        plt.savefig(save_path)
        plt.close()

    def plot_sensitivity_analysis(self, save_path='figure12.png'):
        """
        Generate Figure 12: Sensitivity Analysis
        """
        sensitivity = self.sensitivity_analysis()
        plt.figure(figsize=(10, 6))
        bars = plt.bar(sensitivity.keys(), sensitivity.values())
        plt.title('Sensitivity Analysis of Uncertainty Factors')
        plt.xlabel('Factors')
        plt.ylabel('Contribution (%)')
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}%', ha='center', va='bottom')
        plt.savefig(save_path)
        plt.close()

    def plot_response_time(self, save_path='figure13.png'):
        """
        Generate Figure 13: Response Time Analysis
        """
        plt.figure(figsize=(10, 6))
        sns.histplot(self.results['response_time'], kde=True)
        plt.axvline(2.1, color='g', linestyle='--', label='Target (2.1s)')
        plt.axvline(4.7, color='r', linestyle='--', label='99th Percentile')
        plt.title('Response Time Distribution')
        plt.xlabel('Response Time (seconds)')
        plt.ylabel('Frequency')
        plt.legend()
        plt.savefig(save_path)
        plt.close()

def main():
    # Initialize and run analysis
    analysis = CDSSStatisticalAnalysis()
    analysis.simulate_diagnostic_accuracy()
    
    # Calculate and print statistics
    stats = analysis.calculate_statistics()
    print("\nKey Statistics:")
    print(f"Mean Accuracy: {stats['mean_accuracy']:.1f}%")
    print(f"95% CI: [{stats['ci_95'][0]:.1f}%, {stats['ci_95'][1]:.1f}%]")
    print(f"99th Percentile Response Time: {stats['percentile_99_response']:.2f}s")
    
    # Print sensitivity analysis
    sensitivity = analysis.sensitivity_analysis()
    print("\nSensitivity Analysis:")
    for factor, value in sensitivity.items():
        print(f"{factor}: {value:.1f}%")
    
    # Generate figures
    analysis.plot_diagnostic_accuracy()
    analysis.plot_sensitivity_analysis()
    analysis.plot_response_time()

if __name__ == "__main__":
    main()
