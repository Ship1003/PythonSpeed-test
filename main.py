import time
import sys
import math
from datetime import datetime

class AdvancedProgressBar:
    """
    Advanced progress bar with multiple information displays
    """
    def __init__(self, total, desc="Progress", bar_length=40):
        self.total = total
        self.desc = desc
        self.bar_length = bar_length
        self.start_time = time.time()
        self.current = 0
        self.iteration_times = []
        
    def update(self, current):
        """Update progress bar with performance metrics"""
        self.current = current
        progress = min(current / self.total, 1.0)
        filled_length = int(self.bar_length * progress)
        
        # Create the bar with different colors based on progress
        bar = '█' * filled_length + '▒' * (self.bar_length - filled_length)
        
        # Calculate timing information
        elapsed_time = time.time() - self.start_time
        current_time = datetime.now().strftime("%H:%M:%S")
        
        # Calculate performance metrics
        if elapsed_time > 0:
            speed = current / elapsed_time
            if len(self.iteration_times) >= 2:
                avg_iteration_time = sum(self.iteration_times) / len(self.iteration_times)
                eta = avg_iteration_time * (self.total - current) if current > 0 else 0
            else:
                eta = elapsed_time * (1 - progress) / progress if progress > 0 else 0
        else:
            speed = 0
            eta = 0
            
        # Format ETA
        if eta < 60:
            eta_str = f"{eta:.1f}s"
        elif eta < 3600:
            eta_str = f"{eta/60:.1f}m"
        else:
            eta_str = f"{eta/3600:.1f}h"
            
        # Build progress line
        progress_line = f"\r⏳ {self.desc} |{bar}| {progress*100:6.2f}% "
        progress_line += f"| ⚡ {speed:7.0f}/s | 🕐 {self.format_time(elapsed_time)} "
        progress_line += f"| 🎯 ETA: {eta_str} | 🕒 {current_time}"
        
        sys.stdout.write(progress_line)
        sys.stdout.flush()
        
        # Record iteration time for averaging
        if current > 0:
            iter_time = elapsed_time / current
            self.iteration_times.append(iter_time)
            # Keep only last 100 samples
            if len(self.iteration_times) > 100:
                self.iteration_times.pop(0)
        
    def finish(self):
        """Complete the progress bar"""
        self.update(self.total)
        elapsed = time.time() - self.start_time
        print(f"\n✅ Completed in {self.format_time(elapsed)}")
        
    def format_time(self, seconds):
        """Format time in human readable format"""
        if seconds < 60:
            return f"{seconds:.1f}s"
        elif seconds < 3600:
            m, s = divmod(seconds, 60)
            return f"{m:.0f}m {s:.0f}s"
        else:
            h, m = divmod(seconds, 3600)
            m, s = divmod(m, 60)
            return f"{h:.0f}h {m:.0f}m"

def print_header(text, emoji="✨"):
    """Print formatted header"""
    print("\n" + "═" * 80)
    print(f"{emoji} {text:^74} {emoji}")
    print("═" * 80)

def print_section(title, emoji="📊"):
    """Print formatted section"""
    print(f"\n{emoji} {title}")
    print("─" * 50)

def print_info(key, value, emoji="🔹"):
    """Print information line"""
    print(f"   {emoji} {key:<25}: {value}")

def perform_cycles(num_cycles):
    """
    Execute specified number of cycles with comprehensive monitoring
    """
    print_header(f"EXECUTING {num_cycles:,} CYCLES", "🚀")
    
    # Display execution information
    print_section("EXECUTION INFORMATION", "⚙️")
    print_info("Start Time", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "🕒")
    print_info("Total Cycles", f"{num_cycles:,}", "🔢")
    print_info("Estimated Memory", "Minimal", "💾")
    
    # Start time measurement
    start_time = time.perf_counter_ns()
    start_cpu_time = time.process_time()
    
    # Initialize progress bar
    progress_bar = AdvancedProgressBar(num_cycles, "Processing")
    
    # Performance tracking
    performance_data = {
        'start_memory': 0,  # Could be added with psutil module
        'cycle_times': [],
        'batch_start': time.time()
    }
    
    print_section("REAL-TIME PROGRESS", "📈")
    
    # Execute cycles
    batch_size = max(1, min(num_cycles // 100, 10000))
    
    for i in range(num_cycles):
        # Simulate work - you can add real cycle logic here
        # Example: simple calculation to simulate CPU work
        result = math.sqrt(i) * math.log(i + 1) if i > 0 else 0
        
        # Update progress at calculated intervals
        if i % batch_size == 0 or i == num_cycles - 1:
            progress_bar.update(i + 1)
            
            # Performance sampling (every 10%)
            if i % (num_cycles // 10) == 0 and i > 0:
                current_time = time.time()
                batch_time = current_time - performance_data['batch_start']
                performance_data['batch_start'] = current_time
                performance_data['cycle_times'].append(batch_time / batch_size)
    
    progress_bar.finish()
    
    # End time measurement
    end_time = time.perf_counter_ns()
    end_cpu_time = time.process_time()
    
    # Calculate statistics
    total_time_ns = end_time - start_time
    total_time_sec = total_time_ns / 1_000_000_000
    cpu_time_sec = end_cpu_time - start_cpu_time
    
    return total_time_ns, total_time_sec, cpu_time_sec, performance_data

def format_time(nanoseconds):
    """
    Format time into human readable format with precision
    """
    seconds = nanoseconds / 1_000_000_000
    
    if seconds < 1e-9:
        return f"{nanoseconds:.0f} ns"
    elif seconds < 1e-6:
        return f"{nanoseconds/1000:.2f} µs"
    elif seconds < 1e-3:
        return f"{nanoseconds/1_000_000:.2f} ms"
    elif seconds < 1:
        return f"{seconds:.6f} s"
    elif seconds < 60:
        return f"{seconds:.3f} s"
    else:
        m, s = divmod(seconds, 60)
        if m < 60:
            return f"{m:.0f}m {s:.0f}s"
        else:
            h, m = divmod(m, 60)
            return f"{h:.0f}h {m:.0f}m"

def calculate_performance_metrics(num_cycles, total_time_sec, cpu_time_sec):
    """Calculate comprehensive performance metrics"""
    metrics = {}
    
    # Basic timing
    metrics['total_time'] = total_time_sec
    metrics['cpu_time'] = cpu_time_sec
    metrics['cycles_per_second'] = num_cycles / total_time_sec if total_time_sec > 0 else 0
    metrics['seconds_per_cycle'] = total_time_sec / num_cycles if num_cycles > 0 else 0
    
    # Efficiency
    metrics['cpu_efficiency'] = (cpu_time_sec / total_time_sec) * 100 if total_time_sec > 0 else 0
    
    # Performance rating
    cps = metrics['cycles_per_second']
    if cps >= 10_000_000:
        metrics['rating'] = "🚀 EXTREME"
        metrics['rating_emoji'] = "🚀"
    elif cps >= 1_000_000:
        metrics['rating'] = "⭐ EXCELLENT"
        metrics['rating_emoji'] = "⭐"
    elif cps >= 100_000:
        metrics['rating'] = "💪 GREAT"
        metrics['rating_emoji'] = "💪"
    elif cps >= 10_000:
        metrics['rating'] = "👍 GOOD"
        metrics['rating_emoji'] = "👍"
    elif cps >= 1_000:
        metrics['rating'] = "📊 AVERAGE"
        metrics['rating_emoji'] = "📊"
    else:
        metrics['rating'] = "🐢 SLOW"
        metrics['rating_emoji'] = "🐢"
        
    return metrics

def display_detailed_results(num_cycles, total_ns, total_sec, cpu_time_sec, metrics):
    """Display comprehensive results"""
    print_header("DETAILED PERFORMANCE RESULTS", "📊")
    
    # Timing Information
    print_section("TIMING INFORMATION", "⏱️")
    print_info("Total Execution Time", format_time(total_ns), "⏰")
    print_info("CPU Processing Time", f"{cpu_time_sec:.6f} s", "⚡")
    print_info("Wall Clock Time", f"{total_sec:.6f} s", "🕐")
    print_info("CPU Efficiency", f"{metrics['cpu_efficiency']:.1f}%", "🎯")
    
    # Performance Metrics
    print_section("PERFORMANCE METRICS", "📈")
    print_info("Cycles per Second", f"{metrics['cycles_per_second']:,.0f}", "🔁")
    print_info("Time per Cycle", format_time(metrics['seconds_per_cycle'] * 1e9), "⏳")
    print_info("Performance Rating", f"{metrics['rating']} {metrics['rating_emoji']}", "🏆")
    
    # System Information
    print_section("SYSTEM INFORMATION", "💻")
    print_info("Python Version", sys.version.split()[0], "🐍")
    print_info("Platform", sys.platform, "🖥️")
    print_info("Completion Time", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "✅")

def display_predictions(num_cycles, metrics):
    """Display performance predictions for various cycle counts"""
    print_section("PERFORMANCE PREDICTIONS", "🔮")
    
    test_cycles = [100, 1000, 10000, 100000, 1000000, 10000000, 100000000]
    time_per_cycle = metrics['seconds_per_cycle']
    
    for cycles in test_cycles:
        if cycles > num_cycles:
            estimated_time = time_per_cycle * cycles
            
            if estimated_time < 0.001:
                time_str = f"{estimated_time * 1e6:.1f} µs"
                emoji = "⚡"
            elif estimated_time < 1:
                time_str = f"{estimated_time * 1000:.1f} ms"
                emoji = "🚀"
            elif estimated_time < 60:
                time_str = f"{estimated_time:.2f} s"
                emoji = "⏱️"
            elif estimated_time < 3600:
                time_str = f"{estimated_time/60:.1f} min"
                emoji = "📊"
            else:
                time_str = f"{estimated_time/3600:.2f} hours"
                emoji = "💤"
                
            print_info(f"{cycles:>12,} cycles", f"{time_str} {emoji}", "📅")

def main():
    print_header("ADVANCED CYCLE EXECUTION TIME ANALYZER", "🔬")
    print("Welcome to the comprehensive performance analysis tool!")
    print("This program measures execution time with nanosecond precision")
    print("and provides detailed performance metrics and predictions.\n")
    
    try:
        # Input with validation
        while True:
            cycles_input = input("🎯 Enter number of cycles to execute: ").strip()
            
            if not cycles_input:
                print("❌ Please enter a value. Try again.\n")
                continue
                
            try:
                num_cycles = int(cycles_input.replace(',', '').replace(' ', ''))
                if num_cycles <= 0:
                    print("❌ Number of cycles must be positive. Try again.\n")
                    continue
                break
            except ValueError:
                print("❌ Please enter a valid integer. Try again.\n")
        
        # Large number warning
        if num_cycles > 1_000_000:
            print_section("WARNING", "⚠️")
            print("Large number of cycles detected!")
            estimated_time = num_cycles / 1000000  # Conservative estimate
            if estimated_time > 10:
                print(f"⚠️  This may take approximately {estimated_time:.1f} seconds or more")
            confirm = input("Continue? (y/N): ").lower()
            if confirm not in ['y', 'yes']:
                print("Operation cancelled.")
                return
        
        # Execute and measure
        total_ns, total_sec, cpu_time_sec, performance_data = perform_cycles(num_cycles)
        
        # Calculate metrics
        metrics = calculate_performance_metrics(num_cycles, total_sec, cpu_time_sec)
        
        # Display results
        display_detailed_results(num_cycles, total_ns, total_sec, cpu_time_sec, metrics)
        
        # Display predictions
        display_predictions(num_cycles, metrics)
        
        # Final summary
        print_header("EXECUTION COMPLETE", "🎉")
        print(f"✅ Successfully completed {num_cycles:,} cycles")
        print(f"⚡ Performance: {metrics['cycles_per_second']:,.0f} cycles/second")
        print(f"🏆 Rating: {metrics['rating']}")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Program interrupted by user.")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        print("Please try again with a different number of cycles.")

if __name__ == "__main__":
    main()
    input("\n🎯 Press Enter to exit...")