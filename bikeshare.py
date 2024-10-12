import time
import pandas as pd

# Dữ liệu thành phố
CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

# Hàm lấy thông tin bộ lọc
def get_user_input(prompt, options):
    while True:
        user_input = input(prompt).lower()
        if user_input in options:
            return user_input
        if input(f"Invalid input. Try again? (Y/N): ").lower() not in ['yes', 'y']:
            return None

def get_filters():
    print("Welcome to the US Bikeshare Data Explorer!")
    
    city = get_user_input("Choose a city (Chicago, New York City, Washington): ", CITY_DATA.keys())
    if not city:
        return '', '', ''
    
    month = get_user_input("Choose a month (January to June) or 'all': ", 
                           ['january', 'february', 'march', 'april', 'may', 'june', 'all'])
    if not month:
        return '', '', ''
    
    day = get_user_input("Choose a day (Monday to Sunday) or 'all': ", 
                         ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all'])
    if not day:
        return '', '', ''
    
    return city, month, day

# Hàm load dữ liệu
def load_data(city, month, day):
    df = pd.read_csv(CITY_DATA[city])
    
    # Chuyển đổi thời gian
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Day'] = df['Start Time'].dt.weekday
    df['hour'] = df['Start Time'].dt.hour
    
    # Áp dụng bộ lọc tháng
    months = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6}
    if month != 'all':
        df = df[df['Month'] == months[month]]
    
    # Áp dụng bộ lọc ngày
    days = {'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3, 'friday': 4, 'saturday': 5, 'sunday': 6}
    if day != 'all':
        df = df[df['Day'] == days[day]]
    
    return df

# Hàm tính toán các thông số thống kê
def time_stats(df):
    print("\nCalculating The Most Frequent Times of Travel...\n")
    start_time = time.time()

    # Tháng phổ biến nhất
    common_month = df['Month'].mode()[0]
    print(f"Most popular month: {common_month}")

    # Ngày phổ biến nhất
    common_day = df['Day'].mode()[0]
    print(f"Most popular day of the week: {common_day}")

    # Giờ bắt đầu phổ biến nhất
    common_hour = df['hour'].mode()[0]
    print(f"Most popular start hour: {common_hour}")

    print(f"\nThis took {time.time() - start_time} seconds.")

# Hàm chính
def main():
    while True:
        city, month, day = get_filters()
        if not city:
            print("Exiting the program.")
            break
        
        df = load_data(city, month, day)
        
        time_stats(df)
        
        restart = input("\nWould you like to restart? (Y/N): ").lower()
        if restart not in ['yes', 'y']:
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()
