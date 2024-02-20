import {Component, OnInit} from '@angular/core';
import {MissionDataShareService, ThreatReport} from "../services/mission-data-share.service";

@Component({
  selector: 'app-threat-report',
  templateUrl: './threat-report.component.html',
  styleUrls: ['./threat-report.component.scss']
})
export class ThreatReportComponent implements OnInit {
  threatReport: ThreatReport = {
    active_sat_threat_count: 0,
    debris_threat_count: 0,
    inactive_sat_threat_count: 0,
    rocket_body_threat_count: 0,
    total_threat_count: 0
  };

  constructor(private missionDataShare: MissionDataShareService) {
  }

  ngOnInit(): void {
    this.missionDataShare.$mission.subscribe((threatReport: ThreatReport) => {
      console.log(threatReport)
      this.threatReport = threatReport
      }
    )
  }
}
