from repositories.user_repo import ThresholdRepo
from datetime import datetime, timedelta

def FuzzyLogic(temp, humi, fire, threshold_temp, threshold_humi):
    # Temp: 40 - 45, Humi 30 - 35
    # Membership function for Temperature
    def membership_temp_high(temp):
        # 40 - 45
        if temp <= (threshold_temp - 15):
            return 0
        elif temp < threshold_temp:
            return (temp - threshold_temp) / 15
        else:
            return 1

    # Membership function for Humidity
    def membership_humidity_low(humi):
        # 30 - 35
        if humi <= threshold_humi:
            return 1
        elif humi < (threshold_humi + 20):
            return ((threshold_humi + 20) - humi) / 20
        else:
            return 0

    # Fuzzy inference function
    def fuzzy_fire_rule_base(temp, humi, fire):
        temp_high = membership_temp_high(temp)
        humi_low = membership_humidity_low(humi)

        rules = []

        # Rule 1: Temp high + Humi low + Fire -> VERY HIGH
        if fire == 1 and temp_high > 0.5 and humi_low > 0.5:
            rules.append(("VERY_HIGH", min(temp_high, humi_low)))

        # Rule 2: Temp high + Humi high + Fire -> HIGH
        if fire == 1 and temp_high > 0.5 and humi_low <= 0.5:
            rules.append(("HIGH", temp_high))

        # Rule 3: Temp low + Humi low + Fire -> MEDIUM
        if fire == 1 and temp_high <= 0.5 and humi_low > 0.5:
            rules.append(("MEDIUM", humi_low))

        # Rule 4: Temp high + Humi low + No fire -> HIGH
        if fire == 0 and temp_high > 0.5 and humi_low > 0.5:
            rules.append(("HIGH", min(temp_high, humi_low)))

        # Rule 5: Temp low + Humi high + No fire -> LOW
        if fire == 0 and temp_high <= 0.5 and humi_low <= 0.5:
            rules.append(("LOW", 0.5))

        # Fuzzy Score
        score = 0
        for label, weight in rules:
            if label == "LOW":
                score += weight * 3
            elif label == "MEDIUM":
                score += weight * 5
            elif label == "HIGH":
                score += weight * 7
            elif label == "VERY_HIGH":
                score += weight * 9

        if rules:
            score /= len(rules)
        else:
            score = 2

        return score
    score = fuzzy_fire_rule_base(temp, humi, fire)

    if score > 7:
        print("Fire!!")
        return True
    return False


# if __name__ == "__main__":