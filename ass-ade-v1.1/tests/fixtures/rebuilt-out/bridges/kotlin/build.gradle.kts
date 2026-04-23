plugins {
    kotlin("jvm") version "1.9.25"
    application
}

repositories {
    mavenCentral()
}

application {
    mainClass.set("AssAdeBridgeKt")
}
