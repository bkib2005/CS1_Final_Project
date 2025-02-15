class GPSData:
    """
    Contains the reported GPS data at a certain point.
    """

    def __init__(self, latitude, longitude, elevation, time):
        self.latitude = latitude
        self.longitude = longitude
        self.elevation = elevation
        self.time = time

    def __str__(self):
        return f"{self.time}  {self.latitude:.6f}, {self.longitude:.6f} ({self.elevation:.2f})"
