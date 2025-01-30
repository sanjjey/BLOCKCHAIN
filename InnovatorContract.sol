pragma solidity ^0.8.0;

contract InnovatorRegistry {
    struct Project {
        string projectId;
        uint esgScore;
        bool validated;
    }

    mapping(string => Project) public projects;
    address public admin;
    uint public minValidationScore = 90;

    constructor() {
        admin = msg.sender;
    }

    modifier onlyAdmin() {
        require(msg.sender == admin, "Unauthorized");
        _;
    }

    function registerProject(string memory _projectId, uint _esgScore) public onlyAdmin {
        require(_esgScore >= minValidationScore, "ESG score below minimum threshold");
        projects[_projectId] = Project(_projectId, _esgScore, true);
    }

    function setMinScore(uint _newScore) public onlyAdmin {
        minValidationScore = _newScore;
    }
}