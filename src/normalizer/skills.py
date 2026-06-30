class SkillNormalizer:

    mapping = {

        "js": "JavaScript",
        "javascript": "JavaScript",

        "reactjs": "React",
        "react": "React",

        "node": "Node.js",
        "node.js": "Node.js",

        "express": "Express.js",

        "next.js": "Next.js",

        "mysql": "MySQL",

        "mongodb": "MongoDB",

        "docker": "Docker",

        "git": "Git",

        "github": "GitHub",

        "grafana": "Grafana",

        "influxdb": "InfluxDB",

        "aws": "AWS",

        "html": "HTML",

        "css": "CSS",

        "python": "Python",

        "java": "Java",

        "c": "C",

        "c++": "C++"

    }

    @classmethod
    def normalize(cls, skill):

        if not skill:
            return None

        return cls.mapping.get(skill.lower(), skill)