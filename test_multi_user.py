import threading
import time
from robin_stocks.robinhood import globals as g
from robin_stocks.robinhood import helper

def simulated_user_request(user_token, delay, results, index):
    # Set the thread-local token
    helper.update_session('Authorization', f"Bearer {user_token}")
    
    # Simulate some network delay where threads might interleave
    time.sleep(delay)
    
    # Fetch the token that is currently in the session headers
    current_token = g.get_session().headers.get('Authorization')
    
    # Store the result so the main thread can verify
    results[index] = {
        'expected': f"Bearer {user_token}",
        'actual': current_token
    }

def test_concurrency():
    print("Starting concurrency test...")
    results = [None, None]
    
    # Thread 1: Simulating User A logging in
    thread1 = threading.Thread(
        target=simulated_user_request, 
        args=("USER_A_TOKEN", 0.5, results, 0)
    )
    
    # Thread 2: Simulating User B logging in slightly after User A, 
    # but finishing its request before User A
    thread2 = threading.Thread(
        target=simulated_user_request, 
        args=("USER_B_TOKEN", 0.1, results, 1)
    )
    
    thread1.start()
    thread2.start()
    
    thread1.join()
    thread2.join()
    
    user_a_result = results[0]
    user_b_result = results[1]
    
    print(f"User A Expected: {user_a_result['expected']}, Actual: {user_a_result['actual']}")
    print(f"User B Expected: {user_b_result['expected']}, Actual: {user_b_result['actual']}")
    
    assert user_a_result['expected'] == user_a_result['actual'], "Thread 1 state was overwritten!"
    assert user_b_result['expected'] == user_b_result['actual'], "Thread 2 state was overwritten!"
    print("PASS: Thread states are isolated successfully!")

if __name__ == "__main__":
    test_concurrency()
